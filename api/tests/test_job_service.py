import pytest
from app.services.job_service import JobService
from app.schemas.job import JobCreate
from uuid import uuid4

@pytest.mark.asyncio
async def test_job_create(db_session_mock):
    svc = JobService(db_session_mock)
    data = JobCreate(company_id=uuid4(), title="Backend Dev")
    obj = await svc.create(data)
    db_session_mock.add.assert_called_once()
