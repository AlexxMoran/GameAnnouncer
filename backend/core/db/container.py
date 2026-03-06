from functools import lru_cache

from .database import Database
from core.config import get_settings


@lru_cache(maxsize=1)
def get_db() -> Database:
    """Return a process-wide singleton Database instance."""
    settings = get_settings()

    return Database(
        url=str(settings.db.url),
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
    )
