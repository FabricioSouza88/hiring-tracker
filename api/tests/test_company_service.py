import pytest
from app.services.company_service import CompanyService
from app.schemas.company import CompanyCreate

@pytest.mark.asyncio
async def test_company_create(db_session_mock):
    svc = CompanyService(db_session_mock)
    data = CompanyCreate(trade_name="ACME", legal_name="ACME LTDA")
    obj = await svc.create(data)
    db_session_mock.add.assert_called_once()
