import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus

logger = logging.getLogger("uvicorn.error")

class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')

    VERSION: str = "v0.1"
    API_PREFIX: str = f"/api"
    API_NAME: str = "API"
    DEBUG: bool = False

    """
    Security
    """
    # openssl rand -hex 32
    SECRET_KEY: str = "83cd07fdf2c8311cd4ff3d8b4b9aa6d1c3895bfd6fec1a707dba551b1e021bf4"
    ALGORITHM: str = "HS256"
    JWT_TOKEN_PREFIX: str = "Token"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # one week

    """
    Database
    """
    MONGO_HOST: str
    MONGO_PORT: int = 27017
    DATABASE: str
    MONGO_USERNAME: str | None = None
    MONGO_PASSWORD: str | None = None

    users_collection: str = "users"
    """
    CORS
    """
    ENABLE_CORS: bool = False

    """
    SMTP
    """
    EMAILS_ENABLED: bool = True
    SMTP_TLS: bool = True
    SMTP_PORT: int | None = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    TEMPLATE_FOLDER: str = str(Path(__file__).parent / 'templates')


settings = Settings()