import pytest
from app.services.candidate_service import CandidateService
from app.schemas.candidate import CandidateCreate

@pytest.mark.asyncio
async def test_candidate_create(db_session_mock):
    svc = CandidateService(db_session_mock)
    data = CandidateCreate(full_name="Jane Doe", email="jane@example.com")
    obj = await svc.create(data)
    db_session_mock.add.assert_called_once()
