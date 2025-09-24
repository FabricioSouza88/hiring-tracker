from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class CandidateCreate(BaseModel):
    full_name: str
    cpf: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[dict] = None
    profile_summary: Optional[str] = None
    presentation_text: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None

class CandidateUpdate(BaseModel):
    full_name: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[dict] = None
    profile_summary: Optional[str] = None
    presentation_text: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None

class CandidateOut(BaseModel):
    id: UUID
    full_name: str
    cpf: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[dict] = None
    profile_summary: Optional[str] = None
    presentation_text: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None

    class Config:
        from_attributes = True
