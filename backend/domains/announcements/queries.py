from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domains.announcements.model import Announcement
from domains.participants.model import AnnouncementParticipant
from domains.registration.models import RegistrationForm


def _announcement_response_load_options():
    return (
        selectinload(Announcement.game),
        selectinload(Announcement.participants),
        selectinload(Announcement.registration_form).selectinload(
            RegistrationForm.fields
        ),
    )


class AnnouncementQueries:
    """Read-side database access for Announcement entities."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_id(self, announcement_id: int) -> Announcement | None:
        """Fetch a single announcement with organizer loaded."""
        result = await self.session.execute(
            select(Announcement)
            .options(
                selectinload(Announcement.organizer),
                *_announcement_response_load_options(),
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
            .options(*_announcement_response_load_options())
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
            .options(*_announcement_response_load_options())
            .join(Announcement.participants)
            .where(AnnouncementParticipant.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Announcement.created_at.desc())
        )
        announcements = list(data_result.scalars().all())

        return announcements, total
