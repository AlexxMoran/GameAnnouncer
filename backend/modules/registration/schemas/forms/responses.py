from pydantic import BaseModel, ConfigDict, Field

from modules.registration.schemas.forms.fields.responses import FormFieldResponse


class RegistrationFormResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    announcement_id: int
    fields: list[FormFieldResponse] = Field(
        default_factory=list,
        description="List of form fields in this registration form",
    )
