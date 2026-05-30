from pydantic import BaseModel, Field

from modules.registration.schemas.forms.fields.mutations import FormFieldCreate


class RegistrationFormCreate(BaseModel):
    fields: list[FormFieldCreate] = Field(
        default_factory=list,
        description="List of form fields to create with the registration form",
    )


class RegistrationFormUpdate(BaseModel):
    fields: list[FormFieldCreate] | None = Field(
        None, description="List of form fields to update"
    )
