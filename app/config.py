from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = "UpKeep API"
    app_version: str = "0.1.0"
    database_url: str = "sqlite:///./upkeep.db"

    model_config = SettingsConfigDict(env_prefix="UPKEEP_", env_file=".env", extra="ignore")


settings = Settings()
