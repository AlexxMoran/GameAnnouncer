from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession


from domains.announcements.model import Announcement
from domains.announcements.repository import AnnouncementRepository
from domains.announcements.schemas import AnnouncementAction
from domains.users.model import User
from enums import AnnouncementStatus
from exceptions import ValidationException
from core.permissions import authorize_action


async def update_announcement_status(
    announcement: Announcement,
    action: AnnouncementAction,
    user: User,
    session: AsyncSession,
) -> Announcement:
    """
    Transition an announcement to a new status.

    Validates that the current status allows the requested transition,
    applies the new status (and sets end_at when finishing), then
    persists and flushes.

    Raises ValidationException for invalid state transitions.
    """
    authorize_action(user, announcement, "edit")

    if action == AnnouncementAction.FINISH:
        if announcement.status != AnnouncementStatus.LIVE:
            raise ValidationException("Can only finish announcement when it is 'live'")
        announcement.status = AnnouncementStatus.FINISHED
        announcement.end_at = datetime.now(timezone.utc)
    elif action == AnnouncementAction.CANCEL:
        announcement.status = AnnouncementStatus.CANCELLED
    else:
        raise ValidationException(f"Invalid action: {action}")

    repo = AnnouncementRepository(session)
    announcement = await repo.save(announcement)

    return announcement
