from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, Field
from typing import List


class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",  # Ignore extra environment variables
    )

    # Database
    DATABASE_URL: str = "postgresql://reharmonizer_user:dev_password@localhost:5432/reharmonizer"

    # Application
    APP_NAME: str = "Reharmonizer API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # CORS - stored as string, parsed to list via computed field
    cors_origins_str: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        validation_alias="CORS_ORIGINS"
    )

    @computed_field
    @property
    def CORS_ORIGINS(self) -> List[str]:
        """Parse CORS_ORIGINS from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins_str.split(",")]

    # API
    API_V1_PREFIX: str = "/api/v1"


settings = Settings()
