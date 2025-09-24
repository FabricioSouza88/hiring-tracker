# dummy_api/main.py
from fastapi import FastAPI, HTTPException
from datetime import datetime
import uuid
from typing import List

from models import RoleApplication, TriageTask, UpdateStatusRequest, TriageReport

app = FastAPI(title="Dummy Recruiting API")

# memória simples (substitui banco/queue)
TASKS: List[dict] = []
REPORTS: List[dict] = []

# cria uma tarefa dummy inicial para teste
def seed_task():
    applied = RoleApplication(
        id=str(uuid.uuid4()),
        cand_id="cand123",
        cand_name="Fabricio Souza",
        cand_email="fabricio.collins@gmail.com",
        cand_summary="I am a Backend Specialist and Solution Architect with over 10 years of experience in developing and architecting scalable and resilient systems and APIs. My main focus is on backend with .NET (C#) and Java, cloud solution architecture (Azure and AWS), and applying modern patterns such as microservices, event-driven architecture, and clean architecture.",
        cand_linkedin_url="https://www.linkedin.com/in/fabriciosouza88",
        cand_github_url="https://github.com/FabricioSouza88",
        cand_portfolio_url="https://fabriciosouza88.github.io/",
        cand_seniority="Senior",
        cand_skills=[".NET", "Java", "Python", "AI Agents", "Software Architecture", "Cloud"],
        role_id="role123",
        role_title="Software Engineer Senior",
        role_description="Senior Software Engineer with expertise in backend development.",
        role_level="Senior",
        role_required_skills=[".NET", "Java", "Python"],
        role_nice_to_have_skills=["AI Agents", "Software Architecture", "Cloud"],
        created_at=datetime.utcnow(),
        status="pending",
        stage="applied"
    )
    task = TriageTask(
        task_id=str(uuid.uuid4()),
        tenant_id="tenant1",
        candidate_id="cand123",
        idempotency_key=str(uuid.uuid4()),
        created_at=datetime.utcnow(),
        payload={"role_application": applied.model_dump()},
    )
    TASKS.append({"task": task, "status": "pending"})
    print(f"[seed] Task created id={task.task_id}")

seed_task()


@app.get("/getNextTriage", response_model=TriageTask, status_code=200)
def get_next_triage():
    for entry in TASKS:
        # if entry["status"] == "pending":
            # entry["status"] = "reserved"
            return entry["task"].model_dump()
    raise HTTPException(status_code=204, detail="No tasks available")


@app.post("/UpdateStatus")
def update_status(req: UpdateStatusRequest):
    for entry in TASKS:
        if entry["task"].task_id == req.task_id:
            entry["status"] = req.status
            return {"ok": True, "task_id": req.task_id, "status": req.status}
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/UpdateTriageReport")
def update_triage_report(report: TriageReport):
    REPORTS.append(report.model_dump())
    return {"ok": True, "received": report.task_id}


@app.get("/reports")
def list_reports():
    """Debug endpoint to list collected reports."""
    return REPORTS
