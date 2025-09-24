from pydantic import BaseModel, Field
from functools import lru_cache

class Settings(BaseModel):
    amqp_url: str = Field(default="amqp://guest:guest@mq:5672/")
    api_base_url: str = Field(default="http://api:8080/api/v1")
    prefetch: int = Field(default=16)
    concurrency: int = Field(default=32)
    openai_api_key: str | None = None

@lru_cache
def get_settings() -> Settings:
    return Settings()
