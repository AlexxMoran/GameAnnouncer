from sqlalchemy.ext.asyncio import AsyncSession

from modules.announcements.model import Announcement
from operations.create_announcement.contract import CreateAnnouncementContract
from operations.create_announcement.decisions import CreateAnnouncementDecisions
from operations.create_announcement.gateway import CreateAnnouncementGateway


class CreateAnnouncementScenario:
    """Orchestrates the announcement creation operation."""

    def __init__(self, session: AsyncSession) -> None:
        self._gateway = CreateAnnouncementGateway(session)
        self._decisions = CreateAnnouncementDecisions()

    async def run(self, contract: CreateAnnouncementContract) -> Announcement:
        snapshot = await self._gateway.load(contract)
        decision = self._decisions.make(snapshot)
        return await self._gateway.apply(decision)
