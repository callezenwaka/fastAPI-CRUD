# src/config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Server settings
    environment: str = "development"
    port: int = 8000
    api_version: str = "v1"  # Add this line
    
    # Logging
    log_level: str = "INFO"
    
    # Database settings
    db_host: str = "localhost"
    db_port: int = 5432
    db_username: str = "app_user"
    db_password: str = "app_password"
    db_name: str = "app_db"

    @property
    def database_url(self) -> str:
        """Construct the database URL with asyncpg driver"""
        return f"postgresql+asyncpg://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

# Create a settings instance
settings = Settings()