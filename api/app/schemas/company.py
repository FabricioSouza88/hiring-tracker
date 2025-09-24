from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class CompanyCreate(BaseModel):
    trade_name: str
    legal_name: str
    cnpj: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[dict] = None

class CompanyUpdate(BaseModel):
    trade_name: Optional[str] = None
    legal_name: Optional[str] = None
    cnpj: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[dict] = None

class CompanyOut(BaseModel):
    id: UUID
    trade_name: str
    legal_name: str
    cnpj: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[dict] = None

    class Config:
        from_attributes = True
