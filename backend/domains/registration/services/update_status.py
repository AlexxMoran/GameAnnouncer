from sqlalchemy.ext.asyncio import AsyncSession

from domains.participants.model import AnnouncementParticipant
from domains.participants.repository import ParticipantRepository
from domains.registration.models import RegistrationRequest
from domains.registration.repository import RegistrationRequestRepository
from domains.users.model import User
from enums.registration_status import RegistrationStatus
from core.permissions import authorize_action


async def approve(
    registration_request: RegistrationRequest,
    user: User,
    session: AsyncSession,
) -> RegistrationRequest:
    """
    Approve a registration request and create an AnnouncementParticipant if not already present.

    Flushes changes and returns the reloaded request.
    """
    authorize_action(user, registration_request, "approve")

    registration_request.status = RegistrationStatus.APPROVED

    announcement = registration_request.announcement
    participant_repo = ParticipantRepository(session)
    participant = await participant_repo.find_by_announcement_and_user(
        announcement_id=announcement.id,
        user_id=registration_request.user_id,
    )
    if not participant:
        participant = AnnouncementParticipant(
            announcement_id=announcement.id,
            user_id=registration_request.user_id,
            is_qualified=False,
        )
        session.add(participant)

    await session.flush()

    repo = RegistrationRequestRepository(session)
    return await repo.find_by_id(registration_request.id)


async def reject(
    registration_request: RegistrationRequest,
    user: User,
    session: AsyncSession,
    cancellation_reason: str | None = None,
) -> RegistrationRequest:
    """
    Reject a registration request with an optional reason.

    Flushes changes and returns the reloaded request.
    """
    authorize_action(user, registration_request, "reject")

    registration_request.status = RegistrationStatus.REJECTED
    if cancellation_reason:
        registration_request.cancellation_reason = cancellation_reason

    await session.flush()

    repo = RegistrationRequestRepository(session)
    return await repo.find_by_id(registration_request.id)


async def cancel(
    registration_request: RegistrationRequest,
    user: User,
    session: AsyncSession,
) -> RegistrationRequest:
    """
    Cancel a registration request.

    Flushes changes and returns the reloaded request.
    """
    authorize_action(user, registration_request, "cancel")

    registration_request.status = RegistrationStatus.CANCELLED

    await session.flush()

    repo = RegistrationRequestRepository(session)
    return await repo.find_by_id(registration_request.id)
