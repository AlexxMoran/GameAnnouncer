from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from modules.announcements.model import Announcement
from modules.registration.services.upsert_form import UpsertRegistrationFormService
from operations.create_announcement.contract import CreateAnnouncementContract
from operations.create_announcement.structures import (
    CreateAnnouncementDecision,
    CreateAnnouncementSnapshot,
)


class CreateAnnouncementGateway:
    """Translates between create-announcement operation data and ORM state."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def load(
        self,
        contract: CreateAnnouncementContract,
    ) -> CreateAnnouncementSnapshot:
        return CreateAnnouncementSnapshot(
            announcement_data=contract.announcement_in.model_dump(
                exclude={"registration_form"}
            ),
            registration_form=contract.announcement_in.registration_form,
            organizer_id=contract.organizer_id,
        )

    async def apply(self, decision: CreateAnnouncementDecision) -> Announcement:
        announcement = Announcement(
            **decision.announcement_data,
            organizer_id=decision.organizer_id,
            status=decision.status,
            seed_method=decision.seed_method,
        )
        self._session.add(announcement)
        await self._session.flush()

        await UpsertRegistrationFormService(
            session=self._session,
            announcement=announcement,
            registration_form_in=decision.registration_form,
        ).call()

        result = await self._session.execute(
            select(Announcement)
            .options(selectinload(Announcement.organizer))
            .where(Announcement.id == announcement.id)
        )
        return result.scalar_one()
