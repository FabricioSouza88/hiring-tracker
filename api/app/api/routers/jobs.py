from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db
from app.schemas.job import JobCreate, JobOut, JobUpdate
from app.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("", response_model=JobOut, status_code=201)
async def create_job(payload: JobCreate, db: AsyncSession = Depends(get_db)):
    svc = JobService(db)
    obj = await svc.create(payload)
    return obj

@router.get("", response_model=List[JobOut])
async def list_jobs(offset: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    svc = JobService(db)
    items = await svc.list(offset, limit)
    return list(items)

@router.get("/{job_id}", response_model=JobOut)
async def get_job(job_id: UUID, db: AsyncSession = Depends(get_db)):
    svc = JobService(db)
    obj = await svc.get(job_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Job not found")
    return obj

@router.patch("/{job_id}", response_model=JobOut)
async def update_job(job_id: UUID, payload: JobUpdate, db: AsyncSession = Depends(get_db)):
    svc = JobService(db)
    obj = await svc.update(job_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Job not found")
    return obj
