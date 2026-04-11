from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domains.announcements.model import Announcement


class AnnouncementRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_id_for_update(self, announcement_id: int) -> Announcement | None:
        """Fetch and lock an announcement row with SELECT ... FOR UPDATE.

        Used to serialize concurrent operations that depend on participant
        count (e.g. approve).
        """
        result = await self.session.execute(
            select(Announcement)
            .where(Announcement.id == announcement_id)
            .with_for_update()
        )
        return result.scalar_one_or_none()

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
