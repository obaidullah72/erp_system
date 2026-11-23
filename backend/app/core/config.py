import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8", extra="ignore", hide_input_in_errors=True,
    )
    app_name: str = "ERP Foundation"
    environment: Literal["development", "test", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    database_url: SecretStr = SecretStr("postgresql+psycopg://erp@localhost:5432/erp")
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    jwt_secret_key: SecretStr
    jwt_issuer: str = "erp-api"
    jwt_audience: str = "erp-web"
    access_token_minutes: int = 15
    refresh_token_days: int = Field(default=7, ge=1, le=30)
    redis_url: SecretStr = SecretStr("redis://localhost:6379/0")

    @field_validator("database_url")
    @classmethod
    def postgres_only(cls, value):
        if make_url(value.get_secret_value()).drivername != "postgresql+psycopg":
            raise ValueError("DATABASE_URL must use postgresql+psycopg")
        return value

    @field_validator("redis_url")
    @classmethod
    def redis_scheme(cls, value):
        from urllib.parse import urlsplit
        parsed = urlsplit(value.get_secret_value())
        if parsed.scheme not in {"redis", "rediss"} or not parsed.hostname:
            raise ValueError("REDIS_URL must be a redis:// or rediss:// URL")
        return value

    @field_validator("cors_origins")
    @classmethod
    def explicit_origins(cls, values):
        from urllib.parse import urlsplit
        for value in values:
            parsed = urlsplit(value)
            if (parsed.scheme not in {"http", "https"} or not parsed.netloc
                    or parsed.path or parsed.query or parsed.fragment
                    or parsed.username or parsed.password or "*" in value):
                raise ValueError("CORS origins must be explicit HTTP(S) origins without a path")
        return values

    @field_validator("access_token_minutes")
    @classmethod
    def token_lifetime(cls, value):
        if not 1 <= value <= 60:
            raise ValueError("Access token lifetime must be 1–60 minutes")
        return value

    @model_validator(mode="after")
    def production_secrets(self):
        if self.jwt_secret_key and (len(self.jwt_secret_key.get_secret_value()) < 32 or "replace-with" in self.jwt_secret_key.get_secret_value()):
            raise ValueError("JWT_SECRET_KEY must contain at least 32 characters")
        if self.environment == "production":
            if not self.jwt_secret_key:
                raise ValueError("Production requires JWT_SECRET_KEY")
            if not make_url(self.database_url.get_secret_value()).password:
                raise ValueError("Production requires database credentials")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings(_env_file=None) if os.environ.get("ENVIRONMENT") == "test" else Settings()
