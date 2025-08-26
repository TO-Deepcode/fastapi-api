from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import httpx
import time
import asyncio
from hashlib import md5

from app.config import get_settings
from app.deps import cp_key_dependency
from app.clients import get_async_client

settings = get_settings()
app = FastAPI(
    title="Atlas CP Proxy (FastAPI)",
    version="1.0",
    description="CryptoPanic developer API için hafif proxy",
)

# Basit bellek içi cache (isteğe bağlı)
_cache: dict[str, tuple[float, dict]] = {}
_cache_lock = asyncio.Lock()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.ALLOW_ORIGINS.split(",")] if settings.ALLOW_ORIGINS else ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

VALID_FILTERS = {"rising", "hot", "bullish", "bearish", "important", "saved", "lol"}

def cache_key(**params) -> str:
    raw = "&".join(f"{k}={v}" for k,v in sorted(params.items()))
    return md5(raw.encode()).hexdigest()

async def cached_fetch(client: httpx.AsyncClient, url: str, params: dict) -> dict:
    if not settings.ENABLE_HTTP_CACHE:
        r = await client.get(url, params=params)
        return r.json()
    key = cache_key(url=url, **params)
    now = time.time()
    async with _cache_lock:
        if key in _cache:
            ts, data = _cache[key]
            if now - ts < settings.CACHE_TTL_SECONDS:
                return data
        r = await client.get(url, params=params)
        data = r.json()
        _cache[key] = (now, data)
        return data

@app.get("/healthz", tags=["meta"])
async def health():
    return {"status": "ok"}

@app.get("/posts", summary="List CryptoPanic posts via proxy")
async def posts(
    filter: str | None = Query(None, description="Filter param", regex="^(rising|hot|bullish|bearish|important|saved|lol)$"),
    currencies: str | None = Query(None, description="Comma separated symbols e.g. BTC,ETH"),
    page: int = Query(1, ge=1),
    key: str = Depends(cp_key_dependency),
):
    params: dict[str, str | int] = {"auth_token": key, "page": page}
    if filter:
        if filter not in VALID_FILTERS:
            raise HTTPException(422, f"Invalid filter. Allowed: {', '.join(sorted(VALID_FILTERS))}")
        params["filter"] = filter
    if currencies:
        params["currencies"] = currencies

    async with get_async_client() as client:
        try:
            data = await cached_fetch(client, settings.CRYPTOPANIC_API, params)
        except httpx.RequestError as e:
            raise HTTPException(502, f"Upstream error: {e}") from e

    return JSONResponse(content=data)

# Giriş noktası: uvicorn app.main:app