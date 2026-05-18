from pydantic import BaseModel

from enums.registration_trigger import RegistrationTrigger


class ChangeRegistrationRequestStatusContract(BaseModel):
    """Contract for changing a registration request status."""

    registration_request_id: int
    trigger: RegistrationTrigger
    cancellation_reason: str | None = None
