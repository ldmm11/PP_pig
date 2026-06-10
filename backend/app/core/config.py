from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "PP_pig"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Server
    HOST: str
    PORT: int = 8002

    # Database
    DATABASE_URL: str

    # DeepSeek
    DEEPSEEK_API_KEY: str
    DEEPSEEK_API_BASE: str
    DEEPSEEK_MODEL: str

    model_config = {
        "env_file": Path(__file__).parent.parent.parent / ".env",
        "case_sensitive": True
    }


settings = Settings()
