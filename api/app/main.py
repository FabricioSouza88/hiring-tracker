from fastapi import FastAPI
from app.core.config import get_settings
from app.api.routers import health, companies, jobs, candidates

settings = get_settings()

app = FastAPI(title="Hiring Tracker API", version="0.1.0")

app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(companies.router, prefix=settings.api_prefix)
app.include_router(jobs.router, prefix=settings.api_prefix)
app.include_router(candidates.router, prefix=settings.api_prefix)
