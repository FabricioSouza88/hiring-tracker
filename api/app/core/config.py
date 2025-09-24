from functools import lru_cache
from pydantic import BaseModel, Field

class Settings(BaseModel):
    api_prefix: str = "/api/v1"
    api_host: str = "0.0.0.0"
    api_port: int = 8080

    database_url: str = Field(default="postgresql+asyncpg://app:app@db:5432/hiring")
    amqp_url: str = Field(default="amqp://guest:guest@mq:5672/")

    azure_storage_conn_str: str = Field(default="")
    blob_container: str = Field(default="cv")

@lru_cache
def get_settings() -> Settings:
    return Settings()
