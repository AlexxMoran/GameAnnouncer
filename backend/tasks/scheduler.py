from functools import lru_cache
from core.config import get_settings
from core.logger import logger
from taskiq_redis import ListRedisScheduleSource
from taskiq import TaskiqScheduler
from tasks.broker import get_broker


@lru_cache()
def get_scheduler():
    """Get scheduler with Redis schedule source for persistent schedules."""
    try:
        settings = get_settings()
        redis_source = ListRedisScheduleSource(url=settings.redis.url)
    except Exception:
        from taskiq.schedule_sources import LabelScheduleSource

        redis_source = LabelScheduleSource(get_broker())

    return TaskiqScheduler(broker=get_broker(), sources=[redis_source])


async def register_periodic_tasks():
    """Register all periodic tasks in Redis if they don't already exist."""
    from tasks.announcement_tasks import update_announcement_statuses
    from tasks.registration_request_tasks import expire_registration_requests_task

    PERIODIC_TASKS = [
        {
            "task": update_announcement_statuses,
            "cron": "* * * * *",
            "name": "update_announcement_statuses",
        },
        {
            "task": expire_registration_requests_task,
            "cron": "*/5 * * * *",
            "name": "expire_registration_requests_task",
        },
    ]

    redis_source = get_scheduler().sources[0]

    if not hasattr(redis_source, "startup"):
        return

    await redis_source.startup()

    try:
        schedules = await redis_source.get_schedules()
        existing = {schedule.task_name for schedule in schedules}
    except Exception as e:
        logger.warning(f"Could not get existing schedules: {e}")
        existing = set()

    for task_config in PERIODIC_TASKS:
        task = task_config["task"]
        cron = task_config["cron"]
        name = task_config["name"]

        task_name = task.__name__.replace("__taskiq_original", "")
        full_name = f"{task.__module__}:{task_name}"

        if full_name in existing:
            logger.info(f"⏭️  Skipped: {name} (already scheduled)")
            continue

        try:
            await task.schedule_by_cron(redis_source, cron)
            logger.info(f"✓ Scheduled: {name} ({cron})")
        except Exception as e:
            logger.warning(f"Failed to schedule {name}: {e}")


scheduler = get_scheduler()
