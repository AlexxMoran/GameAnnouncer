"""Clear all schedules from Redis."""

import asyncio
from tasks.scheduler import get_scheduler


async def main():
    """Clear all existing schedules."""
    scheduler = get_scheduler()
    redis_source = scheduler.sources[0]

    await redis_source.startup()

    schedules = await redis_source.get_schedules()
    print(f"\n🔍 Found {len(schedules)} schedules in Redis:")

    task_counts = {}
    for schedule in schedules:
        task_name = schedule.task_name
        task_counts[task_name] = task_counts.get(task_name, 0) + 1
        print(
            f"  - {schedule.task_name} | {schedule.cron} | ID: {schedule.schedule_id}"
        )

    print("\n📊 Summary:")
    for task_name, count in task_counts.items():
        print(f"  {task_name}: {count} duplicate(s)")

    # Delete all schedules
    print(f"\n🗑️  Deleting all {len(schedules)} schedules...")
    for schedule in schedules:
        await redis_source.delete_schedule(schedule.schedule_id)
        print(f"  ✓ Deleted: {schedule.task_name} ({schedule.schedule_id})")

    print("\n✅ All schedules cleared!")
    print("ℹ️  Restart backend container to re-register schedules properly.")


if __name__ == "__main__":
    asyncio.run(main())
