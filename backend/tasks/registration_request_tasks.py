from tasks.broker import broker
from core.logger import logger
from core.db.container import get_db
from domains.registration.models import RegistrationRequest
from domains.announcements.model import Announcement
from domains.registration.services.lifecycle import RegistrationLifecycleService
from enums.registration_status import RegistrationStatus
from sqlalchemy import select, and_
from datetime import datetime, timezone


@broker.task
async def expire_registration_requests_task():
    """Expire registration requests that are past their deadline."""
    logger.info("🔄 Checking for expired registration requests...")

    db = get_db()
    async with db.session_factory() as session:
        now = datetime.now(timezone.utc)

        result = await session.execute(
            select(RegistrationRequest, Announcement)
            .join(Announcement)
            .where(
                and_(
                    RegistrationRequest.status == RegistrationStatus.PENDING,
                    Announcement.registration_end_at < now,
                )
            )
        )

        expired_pairs = result.all()

        for registration_request, announcement in expired_pairs:
            lifecycle = RegistrationLifecycleService(
                registration_request,
                announcement,
                session,
            )
            await lifecycle.expire()

        expired_count = len(expired_pairs)

        if expired_count:
            await session.commit()
            logger.info(f"✅ Expired {expired_count} registration requests")
        else:
            logger.debug("No registration requests to expire")

        return expired_count
