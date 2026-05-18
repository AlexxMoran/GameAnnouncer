from pydantic import BaseModel

from modules.registration.schemas import RegistrationRequestCreate


class CreateRegistrationRequestContract(BaseModel):
    """Contract for creating a registration request."""

    registration_request_in: RegistrationRequestCreate
    user_id: int
