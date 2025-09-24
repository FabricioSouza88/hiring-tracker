from __future__ import annotations
import logging
from typing import Dict, Any, List
from domain.models.models import RoleApplication, TriageResult
from agents.agent_base import AgentBase
from .triage_helper import parse_score_and_decision
from domain.interfaces.llm_client import LLMClient, Message
from mcp.mcp_tools import MCPTools

SUMMARY_SYS = "triage_summary_system.md"
SUMMARY_USER = "triage_summary_user.md"
RUBRIC_SYS  = "triage_rubric_system.md"
RUBRIC_USER = "triage_rubric_user.md"
PROMPT_SCOPE = "triage"
LLM_MODEL = "gpt-4.1-mini"

class TriageAgent(AgentBase):
    def __init__(self, llm: LLMClient, tools: MCPTools | None = None) -> None:
        super().__init__(llm, LLM_MODEL, tools, PROMPT_SCOPE)

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load prompts using base class method
        self.llm_model = LLM_MODEL
        self.summary_sys = self._load_prompt(SUMMARY_SYS, "")
        self.summary_user_tpl = self._load_prompt(SUMMARY_USER, "{context}")
        self.rubric_sys = self._load_prompt(RUBRIC_SYS, "")
        self.rubric_user_tpl = self._load_prompt(RUBRIC_USER, "Role:\n{role_title}\n\nCandidate Summary:\n{cand_summary}")

    # ---------- Public API ----------
    def evaluate(self, candidate: RoleApplication) -> tuple[TriageResult, Dict[str, Any]]:
        """Full pipeline: enrich → summarize → rubric → parse."""
        enrich = self._enrich(candidate)
        summary_md = self._summarize(candidate, enrich)
        
        self.logger.info("Summary Markdown generated.", extra={"summary_md": summary_md})

        final_md = self._apply_rubric(
            role_title=getattr(candidate, "role_title", ""),
            role_description=getattr(candidate, "role_description", ""),
            candidate_summary_md=summary_md
        )

        score, decision, feedback, labels = parse_score_and_decision(final_md)

        # fallback heuristics if model didn’t output explicit score/decision
        if score is None or decision is None:
            score, decision, feedback, labels = self._heuristic_fallback(candidate, labels)

        result = TriageResult(
            triage_score=float(score),
            triage_labels=sorted(set(labels)),
            triage_decision=decision,
            triage_feedback=feedback
        )
        artifacts = {
            "summary_md": summary_md,
            "rubric_md": final_md,
            "enrichment": enrich,
        }
        return result, artifacts

    # ---------- Steps ----------
    def _enrich(self, c: RoleApplication) -> Dict[str, Any]:
        """Optional enrichment via MCP tools (best-effort)."""
        enr: Dict[str, Any] = {}
        try:
            if c.cand_linkedin_url:
                li = self.tools.fetch_linkedin(c.cand_linkedin_url)
                if li: enr["linkedin"] = li
        except Exception as ex:
            enr["linkedin_error"] = str(ex)
        try:
            if c.cand_github_url:
                gh = self.tools.fetch_github(c.cand_github_url)
                if gh: enr["github"] = gh
        except Exception as ex:
            enr["github_error"] = str(ex)
        try:
            if c.cand_portfolio_url:
                pf = self.tools.fetch_portfolio(c.cand_portfolio_url)
                if pf: enr["portfolio"] = pf
        except Exception as ex:
            enr["portfolio_error"] = str(ex)
        return enr

    def _summarize(self, c: RoleApplication, enrich: Dict[str, Any]) -> str:
        """
        Produces a short, structured markdown summary for the candidate.
        """
        context = {
            "role_description": self._safe_getattr(c, "role_description"),
            "role_level": self._safe_getattr(c, "role_level"),
            "role_required_skills": self._safe_join_list(c, "role_required_skills"),
            "nice_to_have_skills": self._safe_join_list(c, "role_nice_to_have_skills"),
            "cand_name": self._safe_getattr(c, "cand_name"),
            "cand_seniority": self._safe_getattr(c, "cand_seniority"),
            "cand_skills": self._safe_join_list(c, "cand_skills"),
            "cand_summary": self._safe_getattr(c, "cand_summary"),
            "cand_linkedin_url": self._safe_getattr(c, "cand_linkedin_url"),
            "cand_portfolio_url": self._safe_getattr(c, "cand_portfolio_url"),
            "cand_github_url": self._safe_getattr(c, "cand_github_url"),
            "enrichment_json": _pp_json(enrich) if enrich else "{}",
            "location": self._safe_getattr(c, "cand_location"),
            "role_title": self._safe_getattr(c, "role_title"),
            # Aliases for template compatibility
            "name": self._safe_getattr(c, "cand_name"),
            "email": self._safe_getattr(c, "cand_email"),
            "seniority": self._safe_getattr(c, "cand_seniority"),
            "skills": self._safe_join_list(c, "cand_skills"),
            "resume_text": self._safe_getattr(c, "cand_resume_text"),
            "linkedin_url": self._safe_getattr(c, "cand_linkedin_url"),
            "github_url": self._safe_getattr(c, "cand_github_url"),
            "portfolio_url": self._safe_getattr(c, "cand_portfolio_url"),
            "extra_info": self._safe_getattr(c, "cand_extra_info"),
        }
        user = self._safe_format(self.summary_user_tpl, {"context": _summary_context_md(context), **context})
        
        summary_md = self._generate_llm_response(
            system_prompt=self.summary_sys,
            user_prompt=user,
            temperature=0.2,
            max_tokens=900
        )
        return summary_md

    def _apply_rubric(self, role_title: str = "", role_description: str = "", candidate_summary_md: str = "") -> str:
        """
        Applies the rubric prompt to produce the final formatted decision.
        The rubric should include lines like:
          Score: X/10
          Decision: approved|hold|rejected
          Labels: python, agents, ...
        """
        user = self._safe_format(self.rubric_user_tpl, {
            "role_title": role_title or "",
            "role_description": role_description or "",
            "applied_role": role_description or role_title or "",
            "summary": candidate_summary_md,
        })
        
        final_md = self._generate_llm_response(
            system_prompt=self.rubric_sys,
            user_prompt=user,
            temperature=0.1,
            max_tokens=1200
        )
        return final_md

    # ---------- Fallback ----------
    def _heuristic_fallback(self, c: RoleApplication, labels_seed: List[str]) -> tuple[float, str, str, List[str]]:
        low = (" ".join(c.cand_skills) + " " + (c.cand_summary or "")).lower()
        weights = {"python":1.0, "agents":1.2, "rag":1.0, "azure":0.8, ".net":0.8, "fastapi":0.6, "gcp":0.6}
        score = 0.0
        labels = set(labels_seed or [])
        for k,w in weights.items():
            if k in low:
                score += w
                labels.add(k)
        norm = round(min(score, 4.0)/4.0*10.0, 2)
        decision = "approved" if norm >= 6 else ("hold" if norm >= 4 else "rejected")        
        feedback = f"Heuristic fallback: matched skills {', '.join(sorted(labels))}."
        return norm, decision, feedback, sorted(labels)

# -------- helpers --------
def _pp_json(d: Dict[str, Any]) -> str:
    import json
    return "```json\n" + json.dumps(d, ensure_ascii=False, indent=2) + "\n```"

def _summary_context_md(ctx: Dict[str, Any]) -> str:
    return (
        f"# Candidate\n"
        f"- Name: {ctx.get('name', '')}\n"
        f"- Email: {ctx.get('email', '')}\n"
        f"- Seniority: {ctx.get('seniority', '')}\n"
        f"- Skills: {ctx.get('skills', '')}\n\n"
        f"## Resume (raw)\n{ctx.get('resume_text', '')}\n\n"
        f"## Enrichment (JSON)\n{ctx.get('enrichment_json', '')}\n"
    )
