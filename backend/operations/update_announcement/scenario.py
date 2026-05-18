from sqlalchemy.ext.asyncio import AsyncSession

from modules.announcements.model import Announcement
from operations.update_announcement.contract import UpdateAnnouncementContract
from operations.update_announcement.decisions import UpdateAnnouncementDecisions
from operations.update_announcement.gateway import UpdateAnnouncementGateway


class UpdateAnnouncementScenario:
    """Orchestrates the announcement update operation."""

    def __init__(self, session: AsyncSession) -> None:
        self._gateway = UpdateAnnouncementGateway(session)
        self._decisions = UpdateAnnouncementDecisions()

    async def run(self, contract: UpdateAnnouncementContract) -> Announcement:
        snapshot = await self._gateway.load(contract)
        decision = self._decisions.make(snapshot)
        return await self._gateway.apply(decision)
