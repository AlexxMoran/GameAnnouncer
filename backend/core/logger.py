import logging
from logging.config import dictConfig
from rich.logging import RichHandler
from rich.console import Console

console = Console(color_system="auto")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "rich": {
            "format": "%(message)s",
            "datefmt": "[%X]",
        },
        "default": {
            "format": "%(levelname)s %(asctime)s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "format": '{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}',
        },
    },
    "handlers": {
        "rich": {
            "()": RichHandler,
            "console": console,
            "formatter": "rich",
            "markup": True,
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
            "show_level": True,
            "show_time": True,
            "show_path": True,
        },
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO", "propagate": False},
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "fastapi": {"handlers": ["rich"], "level": "INFO", "propagate": False},
        "sqlalchemy.engine": {
            "handlers": ["rich"],
            "level": "INFO",
            "propagate": False,
        },
        "sqlalchemy.pool": {
            "handlers": ["rich"],
            "level": "WARNING",
            "propagate": False,
        },
        "alembic": {"handlers": ["rich"], "level": "INFO", "propagate": False},
        "gameannouncer": {"handlers": ["rich"], "level": "DEBUG", "propagate": False},
    },
    "root": {"level": "INFO", "handlers": []},
}


def setup_logging():
    dictConfig(LOGGING_CONFIG)


logger = logging.getLogger("gameannouncer")
