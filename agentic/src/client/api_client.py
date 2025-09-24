import httpx
from typing import Optional, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential_jitter
import appconfig

def _client() -> httpx.Client:
    return httpx.Client(
        base_url=appconfig.API_BASE_URL,
        headers={
            "Authorization": f"Bearer {appconfig.API_KEY}",
            "Content-Type": "application/json",
        },
        timeout=appconfig.REQUEST_TIMEOUT_SECONDS,
    )

@retry(stop=stop_after_attempt(lambda: appconfig.MAX_HTTP_RETRIES),
       wait=wait_exponential_jitter(initial=1, max=15))
def get_next(endpoint: str) -> Optional[Dict[str, Any]]:
    with _client() as c:
        r = c.get(endpoint)
        if r.status_code == 204:
            return None
        r.raise_for_status()
        return r.json()

@retry(stop=stop_after_attempt(lambda: appconfig.MAX_HTTP_RETRIES),
       wait=wait_exponential_jitter(initial=1, max=15))
def update_status(task_id: str, status: str) -> None:
    with _client() as c:
        r = c.post("/UpdateStatus", json={"task_id": task_id, "status": status})
        r.raise_for_status()

@retry(stop=stop_after_attempt(lambda: appconfig.MAX_HTTP_RETRIES),
       wait=wait_exponential_jitter(initial=1, max=15))
def post_report(endpoint: str, payload: Dict[str, Any]) -> None:
    with _client() as c:
        r = c.post(endpoint, json=payload)
        r.raise_for_status()
