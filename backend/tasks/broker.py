from core.config import settings
from core.logger import logger
from taskiq_redis import RedisAsyncResultBackend, ListQueueBroker
from taskiq import TaskiqScheduler


redis_async_result = RedisAsyncResultBackend(
    redis_url=settings.redis.url,
)

broker = ListQueueBroker(
    url=settings.redis.url).with_result_backend(redis_async_result)


scheduler = TaskiqScheduler(broker=broker, sources=[])


async def startup_broker():
    """Start broker if not in worker process."""
    if not broker.is_worker_process:
        await broker.startup()
        logger.info("✓ Taskiq broker started")


async def shutdown_broker():
    """Shutdown broker if not in worker process."""
    if not broker.is_worker_process:
        await broker.shutdown()
        logger.info("✓ Taskiq broker stopped")
