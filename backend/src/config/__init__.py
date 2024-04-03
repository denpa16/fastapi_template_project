from pydantic_settings import BaseSettings

from .settings import (
    AppSettings,
    PostgresSettings,
)


class Settings(BaseSettings):
    """Настройки."""

    app: AppSettings = AppSettings()
    postgres: PostgresSettings = PostgresSettings()


settings = Settings()
