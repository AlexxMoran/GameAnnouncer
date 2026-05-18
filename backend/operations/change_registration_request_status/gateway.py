from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import AppException, ValidationException
from modules.announcements.repository import AnnouncementRepository
from modules.participants.model import AnnouncementParticipant
from modules.participants.repository import ParticipantRepository
from modules.registration.models import RegistrationRequest
from modules.registration.queries import RegistrationRequestQueries
from operations.change_registration_request_status.contract import (
    ChangeRegistrationRequestStatusContract,
)
from operations.change_registration_request_status.structures import (
    ChangeRegistrationRequestStatusDecision,
    ChangeRegistrationRequestStatusSnapshot,
)


class ChangeRegistrationRequestStatusGateway:
    """Translates between ORM state and registration lifecycle operation data."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._participant_repo = ParticipantRepository(session)
        self._registration_request: RegistrationRequest | None = None

    async def load(
        self,
        contract: ChangeRegistrationRequestStatusContract,
    ) -> ChangeRegistrationRequestStatusSnapshot:
        registration_request = await self._load_registration_request(
            contract.registration_request_id
        )
        self._registration_request = registration_request
        announcement = registration_request.announcement

        return ChangeRegistrationRequestStatusSnapshot(
            registration_request_id=registration_request.id,
            announcement_id=announcement.id,
            user_id=registration_request.user_id,
            status=registration_request.status,
            cancellation_reason=contract.cancellation_reason,
        )

    async def apply(
        self,
        decision: ChangeRegistrationRequestStatusDecision,
    ) -> RegistrationRequest:
        assert self._registration_request is not None, "load() must be called before apply()"
        registration_request = self._registration_request

        if decision.check_capacity:
            locked = await AnnouncementRepository(self._session).find_by_id_for_update(
                decision.announcement_id
            )
            if not locked:
                raise ValidationException("Announcement not found")

            participant_count = await self._participant_repo.count_by_announcement_id(
                decision.announcement_id
            )
            if participant_count >= locked.max_participants:
                raise ValidationException(
                    "Cannot approve: maximum number of participants reached"
                )

        registration_request.status = decision.new_status
        if decision.cancellation_reason:
            registration_request.cancellation_reason = decision.cancellation_reason

        if decision.create_participant:
            await self._create_participant_if_missing(decision)

        if decision.delete_participant:
            await self._participant_repo.delete_by_announcement_and_user(
                announcement_id=decision.announcement_id,
                user_id=decision.user_id,
            )

        await self._session.flush()
        return registration_request

    async def _create_participant_if_missing(
        self,
        decision: ChangeRegistrationRequestStatusDecision,
    ) -> None:
        participant = await self._participant_repo.find_by_announcement_and_user(
            announcement_id=decision.announcement_id,
            user_id=decision.user_id,
        )
        if participant:
            return

        self._session.add(
            AnnouncementParticipant(
                announcement_id=decision.announcement_id,
                user_id=decision.user_id,
                is_qualified=False,
            )
        )

    async def _load_registration_request(
        self,
        registration_request_id: int,
    ) -> RegistrationRequest:
        registration_request = await RegistrationRequestQueries(
            self._session
        ).find_by_id(registration_request_id)
        if registration_request is None:
            raise AppException("Registration Request not found", status_code=404)
        return registration_request
