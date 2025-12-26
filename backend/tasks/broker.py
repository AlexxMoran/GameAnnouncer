from functools import lru_cache
from core.config import get_settings
from core.logger import logger
from taskiq_redis import RedisAsyncResultBackend, ListQueueBroker
from taskiq import TaskiqScheduler


@lru_cache
def get_broker():
    settings = get_settings()

    redis_async_result = RedisAsyncResultBackend(
        redis_url=settings.redis.url,
    )

    broker = ListQueueBroker(url=settings.redis.url).with_result_backend(
        redis_async_result
    )

    return broker


@lru_cache
def get_scheduler():
    return TaskiqScheduler(broker=get_broker(), sources=[])


async def startup_broker():
    """Start broker if not in worker process."""
    broker = get_broker()

    if not broker.is_worker_process:
        await broker.startup()
        logger.info("✓ Taskiq broker started")


async def shutdown_broker():
    """Shutdown broker if not in worker process."""
    broker = get_broker()

    if not broker.is_worker_process:
        await broker.shutdown()
        logger.info("✓ Taskiq broker stopped")
