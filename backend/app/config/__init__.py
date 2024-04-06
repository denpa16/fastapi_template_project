from pydantic_settings import BaseSettings

from .settings import (
    DatabaseSettings,
    AppSettings,
)


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    app: AppSettings = AppSettings()


settings = Settings()
