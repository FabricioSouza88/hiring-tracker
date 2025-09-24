import httpx
from .settings import get_settings

class ApiClient:
    def __init__(self):
        s = get_settings()
        self.client = httpx.AsyncClient(base_url=s.api_base_url, timeout=30.0)

    async def close(self):
        await self.client.aclose()

    async def post_agent_run(self, payload: dict):
        # Placeholder endpoint - ajustar quando API expuser /agents/runs
        return await self.client.post("/agents/runs", json=payload)

    async def post_agent_report(self, payload: dict):
        return await self.client.post("/agents/reports", json=payload)
