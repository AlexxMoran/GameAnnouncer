from tasks.broker import broker
from core.logger import logger
from core.db.container import get_db
from modules.registration.models import RegistrationRequest
from modules.announcements.model import Announcement
from enums.registration_status import RegistrationStatus
from enums.registration_trigger import RegistrationTrigger
from operations.change_registration_request_status.contract import (
    ChangeRegistrationRequestStatusContract,
)
from operations.change_registration_request_status.scenario import (
    ChangeRegistrationRequestStatusScenario,
)
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
            await ChangeRegistrationRequestStatusScenario(session).run(
                ChangeRegistrationRequestStatusContract(
                    registration_request_id=registration_request.id,
                    trigger=RegistrationTrigger.EXPIRE,
                )
            )

        expired_count = len(expired_pairs)

        if expired_count:
            await session.commit()
            logger.info(f"✅ Expired {expired_count} registration requests")
        else:
            logger.debug("No registration requests to expire")

        return expired_count
