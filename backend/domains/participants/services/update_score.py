from sqlalchemy.ext.asyncio import AsyncSession

from domains.announcements.model import Announcement
from domains.participants.model import AnnouncementParticipant
from domains.participants.repository import ParticipantRepository
from domains.users.model import User
from exceptions import AppException
from core.permissions import authorize_action


async def update_participant_score(
    participant_id: int,
    qualification_score: int,
    announcement: Announcement,
    user: User,
    session: AsyncSession,
) -> AnnouncementParticipant:
    """
    Update the qualification score for a participant.

    Authorizes that the user has edit rights on the announcement,
    then sets the qualification_score and persists the record.

    Raises AppException(404) if the participant is not found within
    the given announcement.
    """
    authorize_action(user, announcement, "edit")

    repo = ParticipantRepository(session)
    participant = await repo.find_by_id_in_announcement(participant_id, announcement.id)
    if not participant:
        raise AppException("Participant not found", status_code=404)

    participant.qualification_score = qualification_score
    return await repo.save(participant)
