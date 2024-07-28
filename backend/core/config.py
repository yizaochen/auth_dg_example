import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):

    # Database
    DB_PATH: str = os.getenv("DB_PATH")
    DATABASE_URL: str = f"sqlite:///{DB_PATH}"

    # JWT
    ACCESS_TOKEN_SECRET: str = os.getenv("ACCESS_TOKEN_SECRET")
    REFRESH_TOKEN_SECRET: str = os.getenv("REFRESH_TOKEN_SECRET")
    AUTH_ALGORITHM: str = os.getenv("AUTH_ALGORITHM")


def get_settings() -> Settings:
    return Settings()
