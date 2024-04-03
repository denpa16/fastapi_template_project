from pydantic_settings import BaseSettings

from .settings import (
    AppSettings,
)


class Settings(BaseSettings):
    """Настройки."""

    app: AppSettings = AppSettings()


settings = Settings()
