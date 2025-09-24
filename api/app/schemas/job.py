from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class JobCreate(BaseModel):
    company_id: UUID
    title: str
    description: Optional[str] = None
    test_description: Optional[str] = None
    seniority: Optional[str] = None
    location_type: Optional[str] = None
    is_active: Optional[bool] = True

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    test_description: Optional[str] = None
    seniority: Optional[str] = None
    location_type: Optional[str] = None
    is_active: Optional[bool] = None

class JobOut(BaseModel):
    id: UUID
    company_id: UUID
    title: str
    description: Optional[str] = None
    test_description: Optional[str] = None
    seniority: Optional[str] = None
    location_type: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True
