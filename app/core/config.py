from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    database_url: str = "sqlite+pysqlite:///:memory:"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
