from __future__ import annotations

from typing import TYPE_CHECKING

from transitions.core import MachineError
from transitions.extensions.asyncio import AsyncMachine

from enums.registration_status import RegistrationStatus
from enums.registration_trigger import RegistrationTrigger
from exceptions import ValidationException

if TYPE_CHECKING:
    from domains.registration.models import RegistrationRequest


class RegistrationStateMachine:
    """
    State machine for registration request lifecycle.

    Enforces valid status transitions only. Authorization and side effects
    (participant creation/deletion, capacity checks) are the caller's
    responsibility and must be performed in the lifecycle service.

    Usage:
        sm = RegistrationStateMachine(request)
        await sm.fire(RegistrationTrigger.APPROVE)
    """

    states = [s.value for s in RegistrationStatus]

    transitions = [
        {
            "trigger": RegistrationTrigger.APPROVE.value,
            "source": RegistrationStatus.PENDING.value,
            "dest": RegistrationStatus.APPROVED.value,
        },
        {
            "trigger": RegistrationTrigger.REJECT.value,
            "source": RegistrationStatus.PENDING.value,
            "dest": RegistrationStatus.REJECTED.value,
        },
        {
            "trigger": RegistrationTrigger.CANCEL.value,
            "source": RegistrationStatus.PENDING.value,
            "dest": RegistrationStatus.CANCELLED.value,
        },
        {
            "trigger": RegistrationTrigger.CANCEL.value,
            "source": RegistrationStatus.APPROVED.value,
            "dest": RegistrationStatus.CANCELLED.value,
        },
        {
            "trigger": RegistrationTrigger.EXPIRE.value,
            "source": RegistrationStatus.PENDING.value,
            "dest": RegistrationStatus.EXPIRED.value,
        },
        {
            "trigger": RegistrationTrigger.SYSTEM_REJECT.value,
            "source": RegistrationStatus.PENDING.value,
            "dest": RegistrationStatus.REJECTED.value,
        },
        {
            "trigger": RegistrationTrigger.SYSTEM_REJECT.value,
            "source": RegistrationStatus.APPROVED.value,
            "dest": RegistrationStatus.REJECTED.value,
        },
    ]

    def __init__(self, request: RegistrationRequest) -> None:
        self._request = request
        AsyncMachine(
            model=self,
            states=self.states,
            transitions=self.transitions,
            initial=(
                request.status.value
                if isinstance(request.status, RegistrationStatus)
                else request.status
            ),
            auto_transitions=False,
            ignore_invalid_triggers=False,
        )

    async def fire(self, trigger: RegistrationTrigger) -> RegistrationStatus:
        """
        Fire a lifecycle trigger and return the new status.

        Raises:
            ValidationException: If the trigger is not valid from the current status.
        """
        try:
            await getattr(self, trigger.value)()
        except MachineError:
            raise ValidationException(
                f"'{trigger.value}' is not allowed when status is '{self._request.status}'"
            )
        return RegistrationStatus(self.state)
