from sqlalchemy.ext.asyncio import AsyncSession

from domains.announcements.model import Announcement
from domains.participants.model import AnnouncementParticipant
from domains.participants.repository import ParticipantRepository
from exceptions import AppException


async def update_participant_score(
    participant_id: int,
    qualification_score: int,
    announcement: Announcement,
    session: AsyncSession,
) -> AnnouncementParticipant:
    """
    Update the qualification score for a participant.

    Sets the qualification_score and persists the record.

    Raises AppException(404) if the participant is not found within
    the given announcement.
    """
    repo = ParticipantRepository(session)
    participant = await repo.find_by_id_in_announcement(participant_id, announcement.id)
    if not participant:
        raise AppException("Participant not found", status_code=404)

    participant.qualification_score = qualification_score
    return await repo.save(participant)
