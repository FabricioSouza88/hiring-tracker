from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime

class RoleApplication(BaseModel):
    id: str
    cand_id: str
    cand_name: Optional[str] = None
    cand_summary: Optional[str] = None
    cand_email: Optional[str] = None
    cand_seniority: Optional[str] = None
    cand_skills: List[str] = []
    cand_linkedin_url: Optional[str] = None
    cand_portfolio_url: Optional[str] = None
    cand_github_url: Optional[str] = None
    role_id: str
    role_title: str
    role_description: str
    role_level: Optional[str] = None  # Junior, Pleno, Senior
    role_required_skills: List[str] = []
    role_nice_to_have_skills: List[str] = []
    created_at: datetime
    status: str
    stage: str

class TriageTask(BaseModel):
    task_id: str
    tenant_id: str
    candidate_id: str
    idempotency_key: str
    created_at: datetime
    payload: Dict[str, Any]  # {"candidate": {...}}

class TriageResult(BaseModel):
    triage_score: float
    triage_labels: List[str]
    triage_feedback: str
    triage_decision: str  # "approved" | "hold" | "rejected"

class TriageReportPayload(BaseModel):
    task_id: str
    tenant_id: str
    candidate_id: str
    result: TriageResult
    artifacts: Dict[str, Any] = {}
