from typing import Optional
from models.user import User
from models.announcement import Announcement

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from schemas.announcement import (
    AnnouncementCreate,
    AnnouncementUpdate,
    AnnouncementResponse,
)
from core.permissions import authorize_action


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

    async def get_all_count_by_game_id(
        self, session: AsyncSession, game_id: int
    ) -> int:
        result = await session.execute(
            select(func.count(Announcement.id)).where(Announcement.game_id == game_id)
        )
        return result.scalar_one()

    async def get_all_by_organizer_id(
        self, session: AsyncSession, organizer_id: int, skip: int = 0, limit: int = 10
    ) -> list[Announcement]:
        result = await session.execute(
            select(Announcement)
            .where(Announcement.organizer_id == organizer_id)
            .offset(skip)
            .limit(limit)
            .order_by(Announcement.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_all_by_participant_id(
        self, session: AsyncSession, user_id: int, skip: int = 0, limit: int = 10
    ) -> list[Announcement]:
        result = await session.execute(
            select(Announcement)
            .join(Announcement.participants)
            .where(User.id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Announcement.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_participants_by_announcement_id(
        self,
        session: AsyncSession,
        announcement: AnnouncementResponse,
        skip: int = 0,
        limit: int = 10,
    ) -> list[User]:
        result = await session.execute(
            select(User)
            .join(Announcement.participants)
            .where(Announcement.id == announcement.id)
            .offset(skip)
            .limit(limit)
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
        user: User,
        action: str,
    ) -> Announcement:
        authorize_action(user, announcement, action)
        update_data = announcement_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(announcement, field, value)

        await session.commit()
        await session.refresh(announcement)

        return announcement

    async def delete(
        self, session: AsyncSession, announcement: Announcement, user: User, action: str
    ) -> None:
        authorize_action(user, announcement, action)

        await session.delete(announcement)
        await session.commit()


announcement_crud = AnnouncementCRUD()
