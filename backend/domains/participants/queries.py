from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domains.participants.model import AnnouncementParticipant


class ParticipantQueries:
    """Read-side database access for announcement participants."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_all_by_announcement_id(
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
            .order_by(
                AnnouncementParticipant.qualification_score.desc().nulls_last(),
                AnnouncementParticipant.created_at,
                AnnouncementParticipant.id,
            )
            .offset(skip)
            .limit(limit)
        )
        participants = list(data_result.scalars().all())

        return participants, total
