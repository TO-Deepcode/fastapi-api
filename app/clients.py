import httpx
from app.config import get_settings

_settings = get_settings()

def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=_settings.REQUEST_TIMEOUT)