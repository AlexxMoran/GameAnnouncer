from enums.registration_status import RegistrationStatus
from enums.registration_trigger import RegistrationTrigger
from exceptions import ValidationException
from operations.change_registration_request_status.structures import (
    ChangeRegistrationRequestStatusDecision,
    ChangeRegistrationRequestStatusSnapshot,
)

TRANSITIONS = {
    (
        RegistrationStatus.PENDING,
        RegistrationTrigger.APPROVE,
    ): RegistrationStatus.APPROVED,
    (
        RegistrationStatus.PENDING,
        RegistrationTrigger.REJECT,
    ): RegistrationStatus.REJECTED,
    (
        RegistrationStatus.PENDING,
        RegistrationTrigger.CANCEL,
    ): RegistrationStatus.CANCELLED,
    (
        RegistrationStatus.APPROVED,
        RegistrationTrigger.CANCEL,
    ): RegistrationStatus.CANCELLED,
    (
        RegistrationStatus.PENDING,
        RegistrationTrigger.EXPIRE,
    ): RegistrationStatus.EXPIRED,
    (
        RegistrationStatus.PENDING,
        RegistrationTrigger.SYSTEM_REJECT,
    ): RegistrationStatus.REJECTED,
    (
        RegistrationStatus.APPROVED,
        RegistrationTrigger.SYSTEM_REJECT,
    ): RegistrationStatus.REJECTED,
}


class ChangeRegistrationRequestStatusDecisions:
    """Business rules for registration request lifecycle changes."""

    def __init__(self, trigger: RegistrationTrigger) -> None:
        self._trigger = trigger

    def make(
        self,
        snapshot: ChangeRegistrationRequestStatusSnapshot,
    ) -> ChangeRegistrationRequestStatusDecision:
        new_status = self._new_status(snapshot.status)
        was_approved = snapshot.status == RegistrationStatus.APPROVED

        return ChangeRegistrationRequestStatusDecision(
            registration_request_id=snapshot.registration_request_id,
            announcement_id=snapshot.announcement_id,
            user_id=snapshot.user_id,
            new_status=new_status,
            cancellation_reason=self._cancellation_reason(snapshot),
            check_capacity=self._trigger == RegistrationTrigger.APPROVE,
            create_participant=self._trigger == RegistrationTrigger.APPROVE,
            delete_participant=(
                was_approved
                and self._trigger
                in {RegistrationTrigger.CANCEL, RegistrationTrigger.SYSTEM_REJECT}
            ),
        )

    def _new_status(self, status: RegistrationStatus) -> RegistrationStatus:
        new_status = TRANSITIONS.get((status, self._trigger))
        if new_status is None:
            raise ValidationException(
                f"'{self._trigger.value}' is not allowed when status is '{status}'"
            )
        return new_status

    def _cancellation_reason(
        self,
        snapshot: ChangeRegistrationRequestStatusSnapshot,
    ) -> str | None:
        if self._trigger in {
            RegistrationTrigger.REJECT,
            RegistrationTrigger.SYSTEM_REJECT,
        }:
            return snapshot.cancellation_reason
        return None
