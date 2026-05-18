from sqlalchemy.ext.asyncio import AsyncSession

from modules.announcements.model import Announcement
from operations.generate_announcement_bracket.contract import (
    GenerateAnnouncementBracketContract,
)
from operations.generate_announcement_bracket.decisions import (
    GenerateAnnouncementBracketDecisions,
)
from operations.generate_announcement_bracket.gateway import (
    GenerateAnnouncementBracketGateway,
)


class GenerateAnnouncementBracketScenario:
    """Orchestrates the full bracket generation business operation."""

    def __init__(self, session: AsyncSession) -> None:
        self._gateway = GenerateAnnouncementBracketGateway(session)
        self._decisions = GenerateAnnouncementBracketDecisions()

    async def run(
        self,
        contract: GenerateAnnouncementBracketContract,
    ) -> Announcement:
        snapshot = await self._gateway.load(contract)
        decision = self._decisions.make(snapshot)
        return await self._gateway.apply(decision)
