from sqlalchemy.ext.asyncio import AsyncSession

from modules.registration.models import RegistrationRequest
from operations.create_registration_request.contract import (
    CreateRegistrationRequestContract,
)
from operations.create_registration_request.decisions import (
    CreateRegistrationRequestDecisions,
)
from operations.create_registration_request.gateway import (
    CreateRegistrationRequestGateway,
)


class CreateRegistrationRequestScenario:
    """Orchestrates registration request creation."""

    def __init__(self, session: AsyncSession) -> None:
        self._gateway = CreateRegistrationRequestGateway(session)
        self._decisions = CreateRegistrationRequestDecisions()

    async def run(
        self,
        contract: CreateRegistrationRequestContract,
    ) -> RegistrationRequest:
        snapshot = await self._gateway.load(contract)
        decision = self._decisions.make(snapshot)
        return await self._gateway.apply(decision)
