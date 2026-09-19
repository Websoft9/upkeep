from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATABASE_URL = f"sqlite:///{PROJECT_ROOT / 'upkeep.db'}"


class Settings(BaseSettings):
    app_title: str = "UpKeep API"
    app_version: str = "0.1.0"
    database_url: str = DEFAULT_DATABASE_URL

    model_config = SettingsConfigDict(env_prefix="UPKEEP_", env_file=".env", extra="ignore")


settings = Settings()
