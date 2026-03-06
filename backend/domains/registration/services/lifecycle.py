from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from domains.announcements.model import Announcement
from domains.announcements.repository import AnnouncementRepository
from domains.participants.model import AnnouncementParticipant
from domains.participants.repository import ParticipantRepository
from domains.registration.models import RegistrationRequest
from domains.registration.state_machine import RegistrationStateMachine
from enums.registration_status import RegistrationStatus
from enums.registration_trigger import RegistrationTrigger
from exceptions import ValidationException

FORM_CHANGED_REASON = (
    "Registration form has been updated by the organizer. "
    "Please submit a new registration request with the updated form."
)


class RegistrationLifecycleService:
    """
    Application service for registration request lifecycle transitions.

    Wraps RegistrationStateMachine and adds side effects: participant
    creation on approve, participant removal on cancel of previously
    approved requests, capacity enforcement.

    Usage:
        service = RegistrationLifecycleService(registration_request, announcement, session)
        await service.approve()
        await session.commit()
    """

    def __init__(
        self,
        registration_request: RegistrationRequest,
        announcement: Announcement,
        session: AsyncSession,
    ) -> None:
        self._registration_request = registration_request
        self._announcement = announcement
        self._session = session
        self._state_machine = RegistrationStateMachine(registration_request)
        self._participant_repo = ParticipantRepository(session)

    async def approve(self) -> RegistrationRequest:
        """
        Approve the request, enforce capacity, and create participant.

        Validates the transition first, then acquires a row-level lock on the
        announcement to serialize concurrent approvals and checks max_participants.
        """
        new_status = await self._state_machine.fire(RegistrationTrigger.APPROVE)

        announcement_repo = AnnouncementRepository(self._session)
        locked = await announcement_repo.find_by_id_for_update(self._announcement.id)
        if not locked:
            raise ValidationException("Announcement not found")

        count = await self._participant_repo.count_by_announcement_id(
            self._announcement.id
        )
        if count >= locked.max_participants:
            raise ValidationException(
                "Cannot approve: maximum number of participants reached"
            )

        self._registration_request.status = new_status

        participant = await self._participant_repo.find_by_announcement_and_user(
            announcement_id=self._announcement.id,
            user_id=self._registration_request.user_id,
        )
        if not participant:
            participant = AnnouncementParticipant(
                announcement_id=self._announcement.id,
                user_id=self._registration_request.user_id,
                is_qualified=False,
            )
            self._session.add(participant)

        await self._session.flush()
        return self._registration_request

    async def reject(
        self,
        reason: str | None = None,
    ) -> RegistrationRequest:
        """Reject a pending request with an optional reason."""
        new_status = await self._state_machine.fire(RegistrationTrigger.REJECT)
        self._registration_request.status = new_status
        if reason:
            self._registration_request.cancellation_reason = reason

        await self._session.flush()
        return self._registration_request

    async def cancel(self) -> RegistrationRequest:
        """
        Cancel the request.

        If the request was APPROVED, removes the associated participant.
        """
        was_approved = self._registration_request.status == RegistrationStatus.APPROVED

        new_status = await self._state_machine.fire(RegistrationTrigger.CANCEL)
        self._registration_request.status = new_status

        if was_approved:
            await self._remove_participant()

        await self._session.flush()
        return self._registration_request

    async def expire(self) -> None:
        """Expire the request (system-driven)."""
        new_status = await self._state_machine.fire(RegistrationTrigger.EXPIRE)
        self._registration_request.status = new_status
        await self._session.flush()

    async def system_reject_for_form_change(self) -> None:
        """
        Reject an active request due to registration form change.

        For APPROVED requests, also removes the associated participant.
        No flush — intended for batch operations where caller controls flush.
        """
        was_approved = self._registration_request.status == RegistrationStatus.APPROVED

        new_status = await self._state_machine.fire(RegistrationTrigger.SYSTEM_REJECT)
        self._registration_request.status = new_status
        self._registration_request.cancellation_reason = FORM_CHANGED_REASON

        if was_approved:
            await self._remove_participant()

    @staticmethod
    async def batch_system_reject(
        requests: list[RegistrationRequest],
        announcement: Announcement,
        session: AsyncSession,
    ) -> None:
        """
        Reject multiple active requests due to form change with bulk participant removal.

        Deletes all affected participants in a single query, then transitions
        each request via the state machine individually.
        """
        if not requests:
            return

        approved_user_ids = [
            r.user_id for r in requests if r.status == RegistrationStatus.APPROVED
        ]
        if approved_user_ids:
            await session.execute(
                delete(AnnouncementParticipant).where(
                    AnnouncementParticipant.announcement_id == announcement.id,
                    AnnouncementParticipant.user_id.in_(approved_user_ids),
                )
            )

        for req in requests:
            sm = RegistrationStateMachine(req)
            new_status = await sm.fire(RegistrationTrigger.SYSTEM_REJECT)
            req.status = new_status
            req.cancellation_reason = FORM_CHANGED_REASON

    async def _remove_participant(self) -> None:
        """Delete the participant record for this request's announcement and user."""
        await self._participant_repo.delete_by_announcement_and_user(
            announcement_id=self._announcement.id,
            user_id=self._registration_request.user_id,
        )
