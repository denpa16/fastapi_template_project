from os import getenv

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    session_secret_key: str = getenv("SECRET_KEY")

    class Config:
        env_prefix = "app_"

    @property
    def logging_config(self) -> dict:
        from uvicorn.config import LOGGING_CONFIG

        base_config = LOGGING_CONFIG
        base_config["formatters"].update(
            app_formatter={
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "{levelprefix} {asctime} [{name}]: {message}",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "style": "{",
            },
        )
        base_config["handlers"].update(
            app_handler={
                "level": "INFO",
                "formatter": "app_formatter",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            }
        )
        base_config["loggers"].update({"": {"handlers": ["app_handler"], "level": "INFO", "propagate": False}})
        return base_config