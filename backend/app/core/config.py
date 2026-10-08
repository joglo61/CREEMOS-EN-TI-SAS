import secrets
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Sistema de Administración de Préstamos"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Sistema de Administración de Préstamos - CREEMOS EN TI SAS"

    DATABASE_URL: str = "sqlite:///./database/prestamos.db"

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    BACKUP_DIR: str = "./backups"
    DATA_DIR: str = "./data"
    RECIBOS_DIR: str = "./recibos"
    LOGS_DIR: str = "./logs"

    CORS_ORIGINS: str = ""
    MAX_UPLOAD_MB: int = 10
    DEFAULT_ADMIN_PASSWORD: str = ""

    ENABLE_DOCS: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
