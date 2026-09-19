from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    typesafe_api_key: str | None = None  # never exposed to client
    gemini_api_key: str | None = None
    openrouter_api_key: str | None = None
    synthetic_only: bool = True
    database_url: str = "sqlite:///./artifacts/hireflow.db"
    log_level: str = "info"


settings = Settings()
