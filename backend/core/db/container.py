from .database import Database
from core.config import get_settings


def create_db():
    settings = get_settings()

    return Database(
        url=str(settings.db.url),
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
    )


db = create_db()
