from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from domains.announcements.model import Announcement
from domains.announcements.state_machine import AnnouncementStateMachine
from enums import AnnouncementTrigger


class AnnouncementLifecycleService:
    """
    Application service for announcement lifecycle transitions.

    Wraps AnnouncementStateMachine and provides named methods for each
    organizer action and system-triggered event. Authorization and any
    business-logic side effects are the caller's responsibility.

    Usage:
        service = AnnouncementLifecycleService(announcement, session)
        announcement = await service.start_qualification()
        await session.commit()
    """

    def __init__(self, announcement: Announcement, session: AsyncSession) -> None:
        self._announcement = announcement
        self._sm = AnnouncementStateMachine(announcement, session)

    async def start_qualification(self) -> Announcement:
        """Start the qualification stage, moving the announcement to LIVE."""
        return await self._sm.fire(AnnouncementTrigger.START_QUALIFICATION)

    async def finalize_qualification(self) -> Announcement:
        """
        Finalize the qualification stage.

        Signals that scoring is complete and the bracket can now be generated.
        Ranking participants and computing seeds must be done before calling this.
        """
        return await self._sm.fire(AnnouncementTrigger.FINALIZE_QUALIFICATION)

    async def generate_bracket(self) -> Announcement:
        """
        Transition the announcement to bracket phase.

        For non-qualification announcements: moves from REGISTRATION_CLOSED to LIVE.
        For post-qualification announcements: stays LIVE and unlocks bracket play.
        Match record creation must be handled by the caller after this returns.
        """
        return await self._sm.fire(AnnouncementTrigger.GENERATE_BRACKET)

    async def cancel(self) -> Announcement:
        """Cancel the announcement from any non-terminal status."""
        return await self._sm.fire(AnnouncementTrigger.CANCEL)

    async def auto_finish(self) -> Announcement:
        """
        Finish the announcement automatically after the final match completes.

        System-triggered — no user authorization is required.
        Sets end_at to the current UTC time before transitioning to FINISHED.
        """
        self._announcement.end_at = datetime.now(timezone.utc)
        return await self._sm.fire(AnnouncementTrigger.AUTO_FINISH)
