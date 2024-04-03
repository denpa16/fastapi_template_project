from typing import Any

from os import getenv
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, validator


class PostgresSettings(BaseSettings):
    """Настройки postgres."""

    scheme: str = "postgresql+asyncpg"
    host: str = getenv("POSTGRES_HOST", "localhost")
    port: str = getenv("POSTGRES_PORT", "5432")
    user: str = getenv("POSTGRES_USER", "postgres")
    password: str = getenv("POSTGRES_PASSWORD", "postgres")
    db: str = getenv("POSTGRES_HOST", "postgres")
    dsn: str | None
    echo: bool = False

    @validator("dsn", pre=True)
    def dsn_build(cls, value: str | None, values: dict[str, Any]) -> str:
        """Подключение."""
        if isinstance(value, str):
            return value

        return PostgresDsn.build(
            scheme=values["scheme"],
            host=values["host"],
            port=values["port"],
            user=values["user"],
            password=values["password"],
            path=f"/{values['db']}",
        )

    class Config:
        env_prefix = "postgres_"
