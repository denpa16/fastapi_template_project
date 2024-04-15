from typing import Any, Optional
from os import getenv

from pydantic import PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Настройки базы данных."""

    scheme: str = "postgresql+asyncpg"
    host: str = getenv("POSTGRES_HOST", "db")
    port: int = getenv("POSTGRES_PORT")
    user: str = getenv("POSTGRES_USER")
    password: str = getenv("POSTGRES_PASSWORD")
    db: str = getenv("POSTGRES_DB")
    dsn: Optional[PostgresDsn] | Optional[str] = None
    echo: bool = False

    @field_validator("dsn", mode="before")
    @classmethod
    def dsn_build(cls, value: Optional[str], values: ValidationInfo) -> Any:
        """Создание dsn БД."""
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme=values.data.get("scheme"),
            username=values.data.get("user"),
            password=values.data.get("password"),
            host=values.data.get("host"),
            path=values.data.get("db"),
        ).unicode_string()

    class Config:
        env_prefix = "postgres_"
