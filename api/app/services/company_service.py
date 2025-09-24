from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.companies import Company
from app.services.repositories import BaseRepository
from app.schemas.company import CompanyCreate, CompanyUpdate

class CompanyService:
    def __init__(self, session: AsyncSession):
        self.repo = BaseRepository[Company](session, Company)

    async def create(self, data: CompanyCreate) -> Company:
        obj = Company(**data.model_dump())
        return await self.repo.add(obj)

    async def get(self, id: UUID) -> Company | None:
        return await self.repo.get(id)

    async def list(self, offset: int = 0, limit: int = 50):
        return await self.repo.list(offset, limit)

    async def update(self, id: UUID, data: CompanyUpdate) -> Company | None:
        obj = await self.repo.get(id)
        if not obj:
            return None
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        return obj
