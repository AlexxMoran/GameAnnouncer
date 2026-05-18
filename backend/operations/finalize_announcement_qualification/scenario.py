from sqlalchemy.ext.asyncio import AsyncSession

from modules.announcements.model import Announcement
from operations.finalize_announcement_qualification.contract import (
    FinalizeAnnouncementQualificationContract,
)
from operations.finalize_announcement_qualification.decisions import (
    FinalizeAnnouncementQualificationDecisions,
)
from operations.finalize_announcement_qualification.gateway import (
    FinalizeAnnouncementQualificationGateway,
)


class FinalizeAnnouncementQualificationScenario:
    """Orchestrates the qualification finalization operation."""

    def __init__(self, session: AsyncSession) -> None:
        self._gateway = FinalizeAnnouncementQualificationGateway(session)
        self._decisions = FinalizeAnnouncementQualificationDecisions()

    async def run(
        self,
        contract: FinalizeAnnouncementQualificationContract,
    ) -> Announcement:
        snapshot = await self._gateway.load(contract)
        decision = self._decisions.make(snapshot)
        return await self._gateway.apply(decision)
