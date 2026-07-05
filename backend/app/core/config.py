from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Veloura AI Stylist"
    environment: str = "development"
    api_v1_str: str = "/api/v1"
    secret_key: str = "change-me"
    database_url: str = "sqlite+pysqlite:///./veloura.db"
    redis_url: str = "redis://localhost:6379/0"
    openai_api_key: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_default_region: str = "us-east-1"
    s3_bucket: str = ""
    pinterest_access_token: str = ""
    pinterest_ad_account_id: str = ""
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])


@lru_cache
def get_settings() -> Settings:
    return Settings()

