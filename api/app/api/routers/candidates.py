from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db
from app.schemas.candidate import CandidateCreate, CandidateOut, CandidateUpdate
from app.services.candidate_service import CandidateService

router = APIRouter(prefix="/candidates", tags=["candidates"])

@router.post("", response_model=CandidateOut, status_code=201)
async def create_candidate(payload: CandidateCreate, db: AsyncSession = Depends(get_db)):
    svc = CandidateService(db)
    obj = await svc.create(payload)
    return obj

@router.get("", response_model=List[CandidateOut])
async def list_candidates(offset: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    svc = CandidateService(db)
    items = await svc.list(offset, limit)
    return list(items)

@router.get("/{candidate_id}", response_model=CandidateOut)
async def get_candidate(candidate_id: UUID, db: AsyncSession = Depends(get_db)):
    svc = CandidateService(db)
    obj = await svc.get(candidate_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return obj

@router.patch("/{candidate_id}", response_model=CandidateOut)
async def update_candidate(candidate_id: UUID, payload: CandidateUpdate, db: AsyncSession = Depends(get_db)):
    svc = CandidateService(db)
    obj = await svc.update(candidate_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return obj
