from typing import Optional
from models.user import User
from models.announcement import Announcement

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.announcement import AnnouncementCreate, AnnouncementUpdate


class AnnouncementCRUD:
    async def get_all_by_game_id(
        self, session: AsyncSession, game_id: int, skip: int = 0, limit: int = 10
    ) -> list[Announcement]:
        result = await session.execute(
            select(Announcement)
            .where(Announcement.game_id == game_id)
            .offset(skip)
            .limit(limit)
            .order_by(Announcement.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(
        self,
        session: AsyncSession,
        announcement_id: int,
        user: Optional[User] = None,
        action: Optional[str] = None,
    ) -> Optional[Announcement]:
        result = await session.execute(
            select(Announcement).where(Announcement.id == announcement_id)
        )

        announcement = result.scalar_one_or_none()

        if announcement and user and action:
            from core.policies.authorize_action import authorize_action

            authorize_action(user, announcement, action)

        return announcement

    async def create(
        self, session: AsyncSession, announcement_in: AnnouncementCreate, user: User
    ) -> Announcement:
        announcement = Announcement(**announcement_in.model_dump())
        announcement.organizer = user
        session.add(announcement)
        await session.commit()
        await session.refresh(announcement)

        return announcement

    async def update(
        self,
        session: AsyncSession,
        announcement: Announcement,
        announcement_in: AnnouncementUpdate,
    ) -> Announcement:
        update_data = announcement_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(announcement, field, value)

        await session.commit()
        await session.refresh(announcement)

        return announcement

    async def delete(self, session: AsyncSession, announcement: Announcement) -> None:
        await session.delete(announcement)
        await session.commit()


announcement_crud = AnnouncementCRUD()
