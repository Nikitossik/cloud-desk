from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    RESOLUTION_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    RESOLUTION_TOKEN_EXPIRE_MINUTES: int
    SQLALCHEMY_DATABASE_URL: str
    HOST: str
    DEBUG: bool

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


setting = Settings()
