from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application Settings configuration.

    This class manages loading configuration from environment variables.
    It uses pydantic-settings for validation and type safety.
    """

    # Database settings
    # Default to local SQLite for development if not specified
    DATABASE_URL: str = "sqlite:///./inventory.db"

    # Application settings
    APP_NAME: str = "Inventory Management System"
    DEBUG_MODE: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """
    Creates a singleton instance of the Settings class.
    Using lru_cache ensures we only load the environment once.
    """
    return Settings()
