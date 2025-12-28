from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings."""

    # Database
    DATABASE_URL: str = "postgresql://reharmonizer_user:dev_password@localhost:5432/reharmonizer"

    # Application
    APP_NAME: str = "Reharmonizer API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # API
    API_V1_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
