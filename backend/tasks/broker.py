from functools import lru_cache
from core.config import get_settings
from core.logger import logger
from taskiq_redis import RedisAsyncResultBackend, ListQueueBroker
from taskiq import TaskiqScheduler, ScheduleSource


class DisabledBroker:
    """Taskiq broker stub used when real broker cannot be initialized.

    - Safe for imports (pytest, scripts, migrations)
    - Tasks are registered but never executed
    - Excluded from lifecycle
    """

    def task(self, func=None, **kwargs):
        def decorator(f):
            logger.debug(
                "Task %s registered on DisabledBroker (skipped)",
                f.__name__,
            )
            return f

        return decorator(func) if func else decorator

    @property
    def is_worker_process(self) -> bool:
        return True

    async def startup(self) -> None:
        return None

    async def shutdown(self) -> None:
        return None


@lru_cache()
def get_broker():
    """Return a Taskiq broker configured from settings.

    If `get_settings()` raises (for example during pytest collection
    before fixtures/monkeypatch run), return a lightweight disabled broker
    so modules can be imported safely.
    """

    try:
        settings = get_settings()
    except Exception as e:
        logger.warning("Taskiq broker disabled, using DisabledBroker", exc_info=e)

        return DisabledBroker()

    redis_async_result = RedisAsyncResultBackend(
        redis_url=settings.redis.url,
    )

    broker = ListQueueBroker(url=settings.redis.url).with_result_backend(
        redis_async_result
    )

    return broker


@lru_cache()
def get_scheduler():
    """Get scheduler with all periodic tasks."""
    from tasks import expire_registration_requests_task, update_announcement_statuses

    source = ScheduleSource()

    source.add_cron(
        expire_registration_requests_task,
        cron="*/5 * * * *",
        labels={"task_name": "expire_registration_requests"},
    )
    source.add_cron(
        update_announcement_statuses,
        cron="* * * * *",
        labels={"task_name": "update_announcement_statuses"},
    )

    return TaskiqScheduler(broker=get_broker(), sources=[source])


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


broker = get_broker()
