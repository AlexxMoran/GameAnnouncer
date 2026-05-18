from sqlalchemy.ext.asyncio import AsyncSession

from modules.matches.model import Match
from operations.submit_match_result.contract import SubmitMatchResultContract
from operations.submit_match_result.decisions import SubmitMatchResultDecisions
from operations.submit_match_result.gateway import SubmitMatchResultGateway


class SubmitMatchResultScenario:
    """Orchestrates match result submission and bracket progression."""

    def __init__(self, session: AsyncSession) -> None:
        self._gateway = SubmitMatchResultGateway(session)
        self._decisions = SubmitMatchResultDecisions()

    async def run(self, contract: SubmitMatchResultContract) -> Match:
        snapshot = await self._gateway.load(contract)
        decision = self._decisions.make(snapshot)
        return await self._gateway.apply(decision)
