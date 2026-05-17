from datetime import datetime, timezone

from sqlalchemy import delete, select, update
from core.utils import as_utc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import set_committed_value

from enums import AnnouncementStatus, SeedMethod
from enums.registration_status import RegistrationStatus
from modules.announcements.model import Announcement
from modules.announcements.schemas import AnnouncementUpdate
from modules.announcements.validators import AnnouncementValidator
from modules.participants.model import AnnouncementParticipant
from modules.registration.models import RegistrationRequest
from modules.registration.services.lifecycle import (
    TOURNAMENT_UPDATED_REASON,
    RegistrationLifecycleService,
)
from modules.registration.services.upsert_form import UpsertRegistrationFormService


class UpdateAnnouncementService:
    """Update an announcement and reset registrations while the tournament has not started."""

    def __init__(
        self,
        session: AsyncSession,
        announcement: Announcement,
        announcement_in: AnnouncementUpdate,
    ) -> None:
        self.session = session
        self.announcement = announcement
        self.announcement_in = announcement_in

    async def call(self) -> Announcement:
        announcement_data = self.announcement_in.model_dump(
            exclude_unset=True,
            exclude={"registration_form"},
        )

        AnnouncementValidator().validate_update(self.announcement, announcement_data)

        await self._update_announcement(announcement_data)

        await UpsertRegistrationFormService(
            session=self.session,
            announcement=self.announcement,
            registration_form_in=self.announcement_in.registration_form,
        ).call()

        await self._reject_active_registration_requests()
        await self._delete_participants()

        return self.announcement

    def _determine_status(self, announcement_data: dict) -> AnnouncementStatus:
        now = datetime.now(timezone.utc)
        registration_start_at = as_utc(
            announcement_data.get(
                "registration_start_at",
                self.announcement.registration_start_at,
            )
        )
        registration_end_at = as_utc(
            announcement_data.get(
                "registration_end_at",
                self.announcement.registration_end_at,
            )
        )

        if registration_start_at > now:
            return AnnouncementStatus.PRE_REGISTRATION
        if registration_end_at > now:
            return AnnouncementStatus.REGISTRATION_OPEN
        return AnnouncementStatus.REGISTRATION_CLOSED

    def _determine_seed_method(self, has_qualification: bool) -> SeedMethod:
        if has_qualification:
            return SeedMethod.QUALIFICATION_SCORE
        return SeedMethod.RANDOM

    async def _update_announcement(self, announcement_data: dict) -> None:
        has_qualification = announcement_data.get(
            "has_qualification", self.announcement.has_qualification
        )
        announcement_data["seed_method"] = self._determine_seed_method(
            has_qualification
        )
        announcement_data["status"] = self._determine_status(announcement_data)
        await self.session.execute(
            update(Announcement)
            .where(Announcement.id == self.announcement.id)
            .values(**announcement_data)
        )
        await self.session.flush()
        await self.session.refresh(self.announcement)

    async def _reject_active_registration_requests(self) -> None:
        result = await self.session.execute(
            select(RegistrationRequest).where(
                RegistrationRequest.announcement_id == self.announcement.id,
                RegistrationRequest.status.in_(
                    [RegistrationStatus.PENDING, RegistrationStatus.APPROVED]
                ),
            )
        )
        active_requests = list(result.scalars().all())
        await RegistrationLifecycleService.batch_system_reject(
            active_requests,
            self.announcement,
            self.session,
            reason=TOURNAMENT_UPDATED_REASON,
        )

    async def _delete_participants(self) -> None:
        await self.session.execute(
            delete(AnnouncementParticipant).where(
                AnnouncementParticipant.announcement_id == self.announcement.id
            )
        )
        set_committed_value(self.announcement, "participants", [])
