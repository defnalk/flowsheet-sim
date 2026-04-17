"""Application configuration via environment variables."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Backend settings loaded from environment or .env file."""

    cors_origins: list[str] = ["http://localhost:3000"]
    debug: bool = False

    model_config = {"env_prefix": "FLOWSHEET_"}


settings = Settings()
