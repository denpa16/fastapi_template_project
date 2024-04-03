from os import getenv

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Настройки приложения."""

    title: str = getenv("PROJECT_TITLE", "fastapi_template")
    secret_key: str = getenv("SECRET_KEY", "my_very_secret_key_1")

    class Config:
        env_prefix = "app_"
