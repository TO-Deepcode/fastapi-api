from fastapi import Header, HTTPException, Depends
from app.config import get_settings

def cp_key_dependency(x_cp_key: str | None = Header(default=None, alias="X-CP-KEY")) -> str:
    settings = get_settings()
    key = x_cp_key or settings.CP_KEY
    if not key:
        raise HTTPException(status_code=401, detail="Missing X-CP-KEY")
    return key