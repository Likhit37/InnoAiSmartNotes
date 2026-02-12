"""
Centralized application configuration.

All environment-based settings are defined here.
This file acts as the single source of truth for configuration.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    APP_NAME: str
    ENV: str

    # Database
    MONGO_URI: str

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
