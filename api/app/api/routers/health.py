from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db
from app.core.config import get_settings

router = APIRouter()

@router.get("/healthz")
async def healthz(db: AsyncSession = Depends(get_db)):
    # simple DB ping
    try:
        await db.execute("SELECT 1")
        db_ok = True
    except Exception:
        db_ok = False
    return {
        "status": "ok",
        "db": db_ok,
        "version": "v1"
    }
