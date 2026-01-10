from tasks.broker import broker
from core.logger import logger
from core.db.container import create_db
from models.registration_request import RegistrationRequest
from models.announcement import Announcement
from enums.registration_status import RegistrationStatus
from sqlalchemy import select, and_
from datetime import datetime, timezone


@broker.task
async def expire_registration_requests_task():
    """Expire registration requests that are past their deadline."""
    logger.info("🔄 Checking for expired registration requests...")

    db = create_db()
    async with db.session_factory() as session:
        now = datetime.now(timezone.utc)

        result = await session.execute(
            select(RegistrationRequest)
            .join(Announcement)
            .where(
                and_(
                    RegistrationRequest.status == RegistrationStatus.PENDING,
                    Announcement.registration_end_at < now,
                )
            )
        )

        expired_requests = result.scalars().all()

        if expired_requests:
            for req in expired_requests:
                req.status = RegistrationStatus.EXPIRED

            await session.commit()
            logger.info(f"✅ Expired {len(expired_requests)} registration requests")
        else:
            logger.debug("No registration requests to expire")

        return len(expired_requests)
