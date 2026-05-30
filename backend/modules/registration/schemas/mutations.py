from pydantic import BaseModel, Field

from modules.registration.schemas.base import RegistrationRequestBase
from modules.registration.schemas.forms.field_responses.mutations import (
    FormFieldResponseCreate,
)


class RegistrationRequestCreate(RegistrationRequestBase):
    form_responses: list[FormFieldResponseCreate] = Field(
        default_factory=list,
        description="Responses to custom registration form fields, if announcement has a registration form",
    )


class RegistrationRequestUpdate(BaseModel):
    status: str | None = Field(
        None, description="The status of the registration request"
    )
