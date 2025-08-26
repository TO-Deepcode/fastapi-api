from pydantic import BaseSettings, AnyHttpUrl, Field
from functools import lru_cache

class Settings(BaseSettings):
    CRYPTOPANIC_API: AnyHttpUrl = "https://cryptopanic.com/api/developer/v2/posts/"
    CP_KEY: str | None = None  # Opsiyonel, header yoksa bu kullanılır
    REQUEST_TIMEOUT: float = 20.0
    ALLOW_ORIGINS: str = "*"  # Virgülle ayır (örn: https://site1.com,https://site2.com)
    ENABLE_HTTP_CACHE: bool = True
    CACHE_TTL_SECONDS: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache
def get_settings() -> Settings:
    return Settings()