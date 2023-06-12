from pydantic import BaseSettings

from .settings import AppSettings, PostgresSettings


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    app: AppSettings = AppSettings()


settings = Settings()
