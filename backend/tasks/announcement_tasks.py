from datetime import datetime, timezone
from sqlalchemy import update
from models.announcement import Announcement
from enums import AnnouncementStatus
from core.db.container import create_db
from tasks.broker import broker


@broker.task
async def update_announcement_statuses():
    """
    Automatically update announcement statuses based on current time:
    - pre_registration → registration_open (when registration_start_at is reached)
    - registration_open → registration_closed (when registration_end_at is reached)
    - registration_closed → live (when start_at is reached)
    """
    now = datetime.now(timezone.utc)

    db = create_db()
    async with db.session_factory() as session:
        await session.execute(
            update(Announcement)
            .where(Announcement.status == AnnouncementStatus.PRE_REGISTRATION)
            .where(Announcement.registration_start_at <= now)
            .values(status=AnnouncementStatus.REGISTRATION_OPEN)
        )

        await session.execute(
            update(Announcement)
            .where(Announcement.status == AnnouncementStatus.REGISTRATION_OPEN)
            .where(Announcement.registration_end_at <= now)
            .values(status=AnnouncementStatus.REGISTRATION_CLOSED)
        )

        await session.execute(
            update(Announcement)
            .where(Announcement.status == AnnouncementStatus.REGISTRATION_CLOSED)
            .where(Announcement.start_at <= now)
            .values(status=AnnouncementStatus.LIVE)
        )

        await session.commit()
