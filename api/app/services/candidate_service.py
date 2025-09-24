from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.candidates import Candidate
from app.services.repositories import BaseRepository
from app.schemas.candidate import CandidateCreate, CandidateUpdate

class CandidateService:
    def __init__(self, session: AsyncSession):
        self.repo = BaseRepository[Candidate](session, Candidate)

    async def create(self, data: CandidateCreate) -> Candidate:
        obj = Candidate(**data.model_dump())
        return await self.repo.add(obj)

    async def get(self, id: UUID) -> Candidate | None:
        return await self.repo.get(id)

    async def list(self, offset: int = 0, limit: int = 50):
        return await self.repo.list(offset, limit)

    async def update(self, id: UUID, data: CandidateUpdate) -> Candidate | None:
        obj = await self.repo.get(id)
        if not obj:
            return None
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        return obj
