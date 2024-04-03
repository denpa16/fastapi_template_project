from typing import Any

from os import getenv
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, validator


class PostgresSettings(BaseSettings):
    """Настройки postgres."""

    scheme: str = "postgresql+asyncpg"
    host: str = getenv("POSTGRES_HOST", "db")
    port: int = getenv("POSTGRES_PORT", "5432")
    user: str = getenv("POSTGRES_USER", "postgres")
    name: str = getenv("POSTGRES_NAME", "postgres")
    password: str = getenv("POSTGRES_PASSWORD", "postgres")
    dsn: str | None = f"{scheme}://{user}:{password}@{host}/{name}"
    echo: bool = False

    @validator("dsn", pre=True)
    def dsn_build(cls, value: str | None, values: dict[str, Any]) -> str:
        """Создание dsn."""
        if isinstance(value, str):
            return value

        return PostgresDsn.build(
            scheme=values["scheme"],
            host=values["host"],
            port=values["port"],
            password=values["password"],
            path=f"/{values['db']}",
        )

    class Config:
        env_prefix = "postgres_"
        case_insensitive = True
