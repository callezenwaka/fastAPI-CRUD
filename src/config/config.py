# src/config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Server settings
    environment: str = "development"
    port: int = 8000
    title: str = "FastAPI store"
    description: str = "This is a fastAPI service"
    api_version: str = "v1"  # Add this line

    # mail
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str = "test@mail.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    
    # Logging
    log_level: str = "INFO"
    
    # Database settings
    db_host: str = "localhost"
    db_port: int = 5432
    db_username: str = "app_user"
    db_password: str = "app_password"
    db_name: str = "app_db"

    # Redis
    redis_host: str ="localhost"
    redis_port: int = 6379
    redis_password: str = ""
    redis_ttl: int = 86400

    # Auth settings
    JWT_SECRET: str
    JWT_ALGORITHM: str

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
Config = Settings()