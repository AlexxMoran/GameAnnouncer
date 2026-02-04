from typing import Optional
from datetime import datetime, timezone
from models.user import User
from models.announcement import Announcement
from models.registration_form import RegistrationForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from models.game import Game
from schemas.announcement import (
    AnnouncementCreate,
    AnnouncementUpdate,
    AnnouncementAction,
)
from core.permissions import authorize_action
from enums import AnnouncementStatus
from exceptions import ValidationException


class AnnouncementCRUD:
    async def get_all_by_organizer_id(
        self, session: AsyncSession, organizer_id: int, skip: int = 0, limit: int = 10
    ) -> tuple[list[Announcement], int]:
        """
        Get paginated announcements by organizer with total count.

        Returns:
            Tuple of (announcements, total_count)
        """
        count_result = await session.execute(
            select(func.count())
            .select_from(Announcement)
            .where(Announcement.organizer_id == organizer_id)
        )
        total = count_result.scalar_one()

        data_result = await session.execute(
            select(Announcement)
            .where(Announcement.organizer_id == organizer_id)
            .offset(skip)
            .limit(limit)
            .order_by(Announcement.created_at.desc())
        )
        announcements = list(data_result.scalars().all())

        return announcements, total

    async def get_all_by_participant_id(
        self, session: AsyncSession, user_id: int, skip: int = 0, limit: int = 10
    ) -> tuple[list[Announcement], int]:
        """
        Get paginated announcements by participant with total count.

        Returns:
            Tuple of (announcements, total_count)
        """
        count_result = await session.execute(
            select(func.count())
            .select_from(Announcement)
            .join(Announcement.participants)
            .where(User.id == user_id)
        )
        total = count_result.scalar_one()

        data_result = await session.execute(
            select(Announcement)
            .join(Announcement.participants)
            .where(User.id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Announcement.created_at.desc())
        )
        announcements = list(data_result.scalars().all())

        return announcements, total

    async def get_participants_by_announcement_id(
        self,
        session: AsyncSession,
        announcement_id: int,
        skip: int = 0,
        limit: int = 10,
    ) -> tuple[list[User], int]:
        """
        Get paginated participants by announcement with total count.

        Returns:
            Tuple of (participants, total_count)
        """
        count_result = await session.execute(
            select(func.count())
            .select_from(User)
            .join(Announcement.participants)
            .where(Announcement.id == announcement_id)
        )
        total = count_result.scalar_one()

        data_result = await session.execute(
            select(User)
            .join(Announcement.participants)
            .where(Announcement.id == announcement_id)
            .offset(skip)
            .limit(limit)
        )
        participants = list(data_result.scalars().all())

        return participants, total

    async def get_by_id(
        self,
        session: AsyncSession,
        announcement_id: int,
        user: Optional[User] = None,
        action: Optional[str] = None,
    ) -> Optional[Announcement]:
        result = await session.execute(
            select(Announcement)
            .options(
                selectinload(Announcement.organizer),
                selectinload(Announcement.game),
                selectinload(Announcement.registration_form).selectinload(
                    RegistrationForm.fields
                ),
            )
            .where(Announcement.id == announcement_id)
        )

        announcement = result.scalar_one_or_none()

        if announcement and user and action:
            authorize_action(user, announcement, action)

        return announcement

    async def create(
        self, session: AsyncSession, announcement_in: AnnouncementCreate, user: User
    ) -> Announcement:
        now = datetime.now(timezone.utc)

        announcement = Announcement(**announcement_in.model_dump())

        game = await session.get(Game, announcement_in.game_id)
        if game and game.image_url:
            announcement.image_url = game.image_url

        if announcement.registration_start_at <= now:
            announcement.status = AnnouncementStatus.REGISTRATION_OPEN
        else:
            announcement.status = AnnouncementStatus.PRE_REGISTRATION

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

    async def update_status(
        self,
        session: AsyncSession,
        announcement: Announcement,
        action: AnnouncementAction,
        user: User,
    ) -> Announcement:
        authorize_action(user, announcement, "edit")

        if action == AnnouncementAction.FINISH:
            if announcement.status != AnnouncementStatus.LIVE:
                raise ValidationException(
                    "Can only finish announcement when it is 'live'"
                )
            announcement.status = AnnouncementStatus.FINISHED
            announcement.end_at = datetime.now(timezone.utc)
        elif action == AnnouncementAction.CANCEL:
            announcement.status = AnnouncementStatus.CANCELLED
        else:
            raise ValidationException(f"Invalid action: {action}")

        await session.commit()
        await session.refresh(announcement)

        return announcement


announcement_crud = AnnouncementCRUD()
