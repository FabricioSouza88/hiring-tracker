# src/main.py
"""
Main entrypoint for the local polling loop.
- Loads env/config
- Sets up structured logging
- Instantiates RouterAgent with injected LLM/MCP clients
- Runs a simple polling loop with backoff-aware sleep
"""

import time
import logging
from typing import List

from core.logging_setup import setup_logging
from agents.router.router_agent import RouterAgent
import appconfig

# --- LLM & MCP dependency injection -----------------------------------------
from domain.interfaces.llm_client import LLMClient, Message
from mcp.mcp_tools import MCPTools, NoopMCPTools


class DummyLLM(LLMClient):
    """
    Minimal, zero-cost LLM stub for local development.
    - For summary: returns a short deterministic markdown summary.
    - For rubric: returns a deterministic rubric result with required fields.
    Replace with a real implementation (OpenAI/Vertex) for production use.
    """
    def generate(self, messages: List[Message], temperature: float = 0.2, max_tokens: int = 1000) -> str:
        # Heuristic: if the user content looks like a rubric request (has "Role description" or "Candidate summary"),
        # return a properly formatted rubric block. Otherwise, return a short summary.
        joined = "\n\n".join(m.content for m in messages if m.content)
        is_rubric = ("Role description:" in joined) or ("Candidate summary:" in joined)

        if is_rubric:
            # Deterministic, rubric-shaped output with the required fields
            return (
                "## Evaluation\n"
                "- Fit: Reasonable overlap with target stack; needs evidence on production systems.\n"
                "- Experience: Demonstrates hands-on exposure to agents/RAG concepts.\n"
                "- Risks: Missing clear proof of ownership/impact; English level unverified.\n\n"
                "Score: 6.5/10\n"
                "Decision: hold\n"
                "Labels: python, agents, rag\n"
            ).strip()

        # Summary default
        return (
            "# Snapshot\n"
            "- Name: N/A (dev mode)\n"
            "- Seniority: N/A\n"
            "- Skills: python, agents, rag\n\n"
            "## Highlights\n"
            "- Experience with agentic patterns and RAG.\n"
            "- Familiar with cloud fundamentals.\n\n"
            "## Risks/Gaps\n"
            "- Needs stronger production evidence.\n\n"
            "## Narrative\n"
            "Candidate shows relevant exposure to AI agents and retrieval patterns. Further validation required.\n"
        ).strip()


def build_llm_client() -> LLMClient:
    """
    Factory to choose which LLM client to use based on env.
    For now, returns DummyLLM. Replace with OpenAI/Vertex when ready.
    """
    # Example (future):
    # if appconfig.llm_provider == "openai":
    #     return OpenAIClient(api_key=appconfig.openai_api_key, model=appconfig.openai_model)
    # elif appconfig.llm_provider == "vertex":
    #     return VertexClient(project=appconfig.gcp_project, model=appconfig.vertex_model)
    return DummyLLM()


def build_mcp_tools() -> MCPTools:
    """
    Factory to choose MCP tools client (e.g., FastAPIMCP).
    For now, returns NoopMCPTools (safe default).
    """
    # Example (future):
    # return FastAPIMCPClient(base_url=appconfig.mcp_base_url, api_key=appconfig.mcp_api_key)
    return NoopMCPTools()


# --- Polling loop ------------------------------------------------------------

def main() -> None:
    setup_logging(appconfig.LOG_LEVEL)
    logging.info("Starting polling loop (API-driven)…")

    llm = build_llm_client()
    tools = build_mcp_tools()
    router = RouterAgent(llm=llm, tools=tools)

    interval = appconfig.POLL_INTERVAL_SECONDS
    # Safety: minimum 1 second interval
    interval = max(1, int(interval))

    while True:
        try:
            # One tick attempts TRIAGE -> TEST -> REPORT in priority order,
            # processing at most one item, and returns True if something was processed.
            processed = router.run_tick()
        except Exception as ex:
            logging.error(f"Tick failed: {ex}", exc_info=True)
            processed = False

        # If we processed an item, we shorten the next sleep to re-check sooner.
        sleep_secs = interval if not processed else max(1, interval // 4)
        time.sleep(sleep_secs)


if __name__ == "__main__":
    main()
