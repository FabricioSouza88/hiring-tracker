from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.jobs import Job
from app.services.repositories import BaseRepository
from app.schemas.job import JobCreate, JobUpdate

class JobService:
    def __init__(self, session: AsyncSession):
        self.repo = BaseRepository[Job](session, Job)

    async def create(self, data: JobCreate) -> Job:
        obj = Job(**data.model_dump())
        return await self.repo.add(obj)

    async def get(self, id: UUID) -> Job | None:
        return await self.repo.get(id)

    async def list(self, offset: int = 0, limit: int = 50):
        return await self.repo.list(offset, limit)

    async def update(self, id: UUID, data: JobUpdate) -> Job | None:
        obj = await self.repo.get(id)
        if not obj:
            return None
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        return obj
