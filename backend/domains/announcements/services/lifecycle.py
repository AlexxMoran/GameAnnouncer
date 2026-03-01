from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from domains.announcements.model import Announcement
from domains.announcements.state_machine import AnnouncementStateMachine
from domains.users.model import User
from enums import AnnouncementTrigger


class AnnouncementLifecycleService:
    """
    Application service for announcement lifecycle transitions.

    Wraps AnnouncementStateMachine and provides named methods for each
    organizer action and system-triggered event. Business logic and side
    effects (e.g. notifications, bracket creation) are the caller's responsibility.

    Usage:
        service = AnnouncementLifecycleService(announcement, session)
        announcement = await service.start_qualification(user)
        await session.commit()
    """

    def __init__(self, announcement: Announcement, session: AsyncSession) -> None:
        self._announcement = announcement
        self._sm = AnnouncementStateMachine(announcement, session)

    async def start_qualification(self, user: User) -> Announcement:
        """Start the qualification stage, moving the announcement to LIVE."""
        return await self._sm.fire(AnnouncementTrigger.START_QUALIFICATION, user=user)

    async def finalize_qualification(self, user: User) -> Announcement:
        """
        Finalize the qualification stage.

        Signals that scoring is complete and the bracket can now be generated.
        Ranking participants and computing seeds must be done before calling this.
        """
        return await self._sm.fire(
            AnnouncementTrigger.FINALIZE_QUALIFICATION, user=user
        )

    async def generate_bracket(self, user: User) -> Announcement:
        """
        Transition the announcement to bracket phase.

        For non-qualification announcements: moves from REGISTRATION_CLOSED to LIVE.
        For post-qualification announcements: stays LIVE and unlocks bracket play.
        Match record creation must be handled by the caller after this returns.
        """
        return await self._sm.fire(AnnouncementTrigger.GENERATE_BRACKET, user=user)

    async def cancel(self, user: User) -> Announcement:
        """Cancel the announcement from any non-terminal status."""
        return await self._sm.fire(AnnouncementTrigger.CANCEL, user=user)

    async def auto_finish(self) -> Announcement:
        """
        Finish the announcement automatically after the final match completes.

        System-triggered — no user authorization is required.
        Sets end_at to the current UTC time before transitioning to FINISHED.
        """
        self._announcement.end_at = datetime.now(timezone.utc)
        return await self._sm.fire(AnnouncementTrigger.AUTO_FINISH, user=None)
