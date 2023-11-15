from os import getenv
from typing import Any

from pydantic import BaseSettings, PostgresDsn, validator


class PostgresSettings(BaseSettings):
    """Конфиги БД."""

    scheme: str = "postgresql+asyncpg"
    host: str = getenv("POSTGRES_HOST")
    port: str = getenv("POSTGRES_PORT")
    user: str = getenv("POSTGRES_USER")
    password: str = getenv("POSTGRES_PASSWORD")
    db: str = getenv("POSTGRES_NAME")
    dsn: str | None
    echo: bool = False

    @validator("dsn", pre=True)
    def dsn_build(cls, value: str | None, values: dict[str, Any]) -> str:
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
