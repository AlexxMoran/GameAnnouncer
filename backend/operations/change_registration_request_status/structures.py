from dataclasses import dataclass

from enums.registration_status import RegistrationStatus


@dataclass(frozen=True)
class ChangeRegistrationRequestStatusSnapshot:
    registration_request_id: int
    announcement_id: int
    user_id: int
    status: RegistrationStatus
    cancellation_reason: str | None


@dataclass(frozen=True)
class ChangeRegistrationRequestStatusDecision:
    registration_request_id: int
    announcement_id: int
    user_id: int
    new_status: RegistrationStatus
    cancellation_reason: str | None
    check_capacity: bool
    create_participant: bool
    delete_participant: bool
