from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import set_committed_value

from enums import AnnouncementStatus
from exceptions import AppException
from modules.announcements.model import Announcement
from modules.participants.repository import ParticipantRepository
from modules.registration.repository import RegistrationRequestRepository
from modules.registration.reasons import TOURNAMENT_UPDATED_REASON
from modules.registration.services.upsert_form import UpsertRegistrationFormService
from operations.update_announcement.contract import UpdateAnnouncementContract
from operations.update_announcement.structures import (
    UpdateAnnouncementDecision,
    UpdateAnnouncementSnapshot,
)
from enums.registration_status import RegistrationStatus


class UpdateAnnouncementGateway:
    """Translates between update-announcement operation data and ORM state."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def load(
        self,
        contract: UpdateAnnouncementContract,
    ) -> UpdateAnnouncementSnapshot:
        announcement = await self._load_announcement(contract.announcement_id)

        return UpdateAnnouncementSnapshot(
            announcement_id=announcement.id,
            status=AnnouncementStatus(announcement.status),
            start_at=announcement.start_at,
            registration_start_at=announcement.registration_start_at,
            registration_end_at=announcement.registration_end_at,
            has_qualification=announcement.has_qualification,
            announcement_data=contract.announcement_in.model_dump(
                exclude_unset=True,
                exclude={"registration_form"},
            ),
            registration_form=contract.announcement_in.registration_form,
        )

    async def apply(self, decision: UpdateAnnouncementDecision) -> Announcement:
        announcement = await self._load_announcement(decision.announcement_id)

        announcement_data = {
            **decision.announcement_data,
            "status": decision.status,
            "seed_method": decision.seed_method,
        }
        await self._session.execute(
            update(Announcement)
            .where(Announcement.id == decision.announcement_id)
            .values(**announcement_data)
        )
        await self._session.flush()
        await self._session.refresh(announcement)

        await UpsertRegistrationFormService(
            session=self._session,
            announcement=announcement,
            registration_form_in=decision.registration_form,
        ).call()

        if decision.reject_active_registration_requests:
            await self._reject_active_registration_requests(announcement)

        if decision.delete_participants:
            await self._delete_participants(announcement)

        return announcement

    async def _load_announcement(self, announcement_id: int) -> Announcement:
        result = await self._session.execute(
            select(Announcement)
            .options(selectinload(Announcement.registration_form))
            .where(Announcement.id == announcement_id)
        )
        announcement = result.scalar_one_or_none()
        if announcement is None:
            raise AppException("Announcement not found", status_code=404)
        return announcement

    async def _reject_active_registration_requests(
        self,
        announcement: Announcement,
    ) -> None:
        active_requests = await RegistrationRequestRepository(
            self._session
        ).find_active_by_announcement_id(announcement.id)
        approved_user_ids = [
            request.user_id
            for request in active_requests
            if request.status == RegistrationStatus.APPROVED
        ]
        await ParticipantRepository(self._session).delete_by_announcement_and_user_ids(
            announcement_id=announcement.id,
            user_ids=approved_user_ids,
        )

        for registration_request in active_requests:
            registration_request.status = RegistrationStatus.REJECTED
            registration_request.cancellation_reason = TOURNAMENT_UPDATED_REASON

    async def _delete_participants(self, announcement: Announcement) -> None:
        await ParticipantRepository(self._session).delete_by_announcement_id(
            announcement.id
        )
        set_committed_value(announcement, "participants", [])
