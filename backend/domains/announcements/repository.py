from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from domains.announcements.model import Announcement
from domains.announcements.participant_model import AnnouncementParticipant


class AnnouncementRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_id(self, announcement_id: int) -> Announcement | None:
        """Fetch a single announcement with organizer and game loaded."""
        result = await self.session.execute(
            select(Announcement)
            .options(
                selectinload(Announcement.organizer),
                selectinload(Announcement.game),
            )
            .where(Announcement.id == announcement_id)
        )
        return result.scalar_one_or_none()

    async def find_all_by_organizer_id(
        self, organizer_id: int, skip: int = 0, limit: int = 10
    ) -> tuple[list[Announcement], int]:
        """Get paginated announcements by organizer with total count."""
        count_result = await self.session.execute(
            select(func.count())
            .select_from(Announcement)
            .where(Announcement.organizer_id == organizer_id)
        )
        total = count_result.scalar_one()

        data_result = await self.session.execute(
            select(Announcement)
            .where(Announcement.organizer_id == organizer_id)
            .offset(skip)
            .limit(limit)
            .order_by(Announcement.created_at.desc())
        )
        announcements = list(data_result.scalars().all())

        return announcements, total

    async def find_all_by_participant_id(
        self, user_id: int, skip: int = 0, limit: int = 10
    ) -> tuple[list[Announcement], int]:
        """Get paginated announcements where the user is a participant."""
        count_result = await self.session.execute(
            select(func.count())
            .select_from(Announcement)
            .join(Announcement.participants)
            .where(AnnouncementParticipant.user_id == user_id)
        )
        total = count_result.scalar_one()

        data_result = await self.session.execute(
            select(Announcement)
            .join(Announcement.participants)
            .where(AnnouncementParticipant.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Announcement.created_at.desc())
        )
        announcements = list(data_result.scalars().all())

        return announcements, total

    async def find_participants_by_announcement_id(
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
            .offset(skip)
            .limit(limit)
        )
        participants = list(data_result.scalars().all())

        return participants, total

    async def save(self, announcement: Announcement) -> Announcement:
        """Persist an announcement (create or update). Flushes but does not commit."""
        self.session.add(announcement)
        await self.session.flush()
        await self.session.refresh(announcement)
        return announcement

    async def delete(self, announcement: Announcement) -> None:
        """Delete an announcement. Flushes but does not commit."""
        await self.session.delete(announcement)
        await self.session.flush()


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

    async def save(
        self, participant: AnnouncementParticipant
    ) -> AnnouncementParticipant:
        """Persist a participant record. Flushes but does not commit."""
        self.session.add(participant)
        await self.session.flush()
        await self.session.refresh(participant)
        return participant
