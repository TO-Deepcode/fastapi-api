# main.py
from fastapi import FastAPI, Header, HTTPException
import httpx, os

API = "https://cryptopanic.com/api/developer/v2/posts/"
app = FastAPI()

@app.get("/posts")
async def posts(filter: str | None = None, currencies: str | None = None, page: int = 1, x_cp_key: str | None = Header(None)):
    key = x_cp_key or os.getenv("CP_KEY")
    if not key: raise HTTPException(401, "Missing X-CP-KEY")
    params = {"auth_token": key, "page": page}
    if filter: params["filter"] = filter
    if currencies: params["currencies"] = currencies
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(API, params=params)
    return r.json()
