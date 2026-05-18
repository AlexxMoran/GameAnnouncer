from sqlalchemy.ext.asyncio import AsyncSession

from modules.registration.models import RegistrationRequest
from operations.change_registration_request_status.contract import (
    ChangeRegistrationRequestStatusContract,
)
from operations.change_registration_request_status.decisions import (
    ChangeRegistrationRequestStatusDecisions,
)
from operations.change_registration_request_status.gateway import (
    ChangeRegistrationRequestStatusGateway,
)


class ChangeRegistrationRequestStatusScenario:
    """Orchestrates registration request lifecycle changes."""

    def __init__(self, session: AsyncSession) -> None:
        self._gateway = ChangeRegistrationRequestStatusGateway(session)

    async def run(
        self,
        contract: ChangeRegistrationRequestStatusContract,
    ) -> RegistrationRequest:
        snapshot = await self._gateway.load(contract)
        decision = ChangeRegistrationRequestStatusDecisions(contract.trigger).make(
            snapshot
        )
        return await self._gateway.apply(decision)
