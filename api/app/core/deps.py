from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from app.core.config import get_settings

_engine = None
_SessionLocal = None

def _init_engine():
    global _engine, _SessionLocal
    settings = get_settings()
    if _engine is None:
        _engine = create_async_engine(settings.database_url, pool_pre_ping=True)
        _SessionLocal = async_sessionmaker(bind=_engine, expire_on_commit=False)

_init_engine()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = _SessionLocal()
    try:
        yield session
    finally:
        await session.close()
