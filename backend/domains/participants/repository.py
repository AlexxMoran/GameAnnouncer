from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from domains.participants.model import AnnouncementParticipant


class ParticipantRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_announcement_and_user(
        self, announcement_id: int, user_id: int
    ) -> AnnouncementParticipant | None:
        """Find a participant record by announcement and user IDs."""
        result = await self.session.execute(
            select(AnnouncementParticipant).where(
                AnnouncementParticipant.announcement_id == announcement_id,
                AnnouncementParticipant.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def find_by_announcement_id(
        self, announcement_id: int, skip: int = 0, limit: int = 10
    ) -> tuple[list[AnnouncementParticipant], int]:
        """Get paginated participants for an announcement."""
        count_result = await self.session.execute(
            select(func.count())
            .select_from(AnnouncementParticipant)
            .where(AnnouncementParticipant.announcement_id == announcement_id)
        )
        total = count_result.scalar_one()

        data_result = await self.session.execute(
            select(AnnouncementParticipant)
            .options(selectinload(AnnouncementParticipant.user))
            .where(AnnouncementParticipant.announcement_id == announcement_id)
            .order_by(AnnouncementParticipant.created_at)
            .offset(skip)
            .limit(limit)
        )
        participants = list(data_result.scalars().all())

        return participants, total

    async def save(
        self, participant: AnnouncementParticipant
    ) -> AnnouncementParticipant:
        """Persist a participant record. Flushes but does not commit."""
        self.session.add(participant)
        await self.session.flush()
        await self.session.refresh(participant)
        return participant
