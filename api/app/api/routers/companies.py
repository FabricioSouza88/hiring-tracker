from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db
from app.schemas.company import CompanyCreate, CompanyOut, CompanyUpdate
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("", response_model=CompanyOut, status_code=201)
async def create_company(payload: CompanyCreate, db: AsyncSession = Depends(get_db)):
    svc = CompanyService(db)
    obj = await svc.create(payload)
    return obj

@router.get("", response_model=List[CompanyOut])
async def list_companies(offset: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    svc = CompanyService(db)
    items = await svc.list(offset, limit)
    return list(items)

@router.get("/{company_id}", response_model=CompanyOut)
async def get_company(company_id: UUID, db: AsyncSession = Depends(get_db)):
    svc = CompanyService(db)
    obj = await svc.get(company_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Company not found")
    return obj

@router.patch("/{company_id}", response_model=CompanyOut)
async def update_company(company_id: UUID, payload: CompanyUpdate, db: AsyncSession = Depends(get_db)):
    svc = CompanyService(db)
    obj = await svc.update(company_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Company not found")
    return obj
