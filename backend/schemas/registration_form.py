from pydantic import BaseModel, Field
from schemas.form_field import FormFieldCreate, FormFieldResponse


class RegistrationFormBase(BaseModel):
    pass


class RegistrationFormCreate(RegistrationFormBase):
    fields: list[FormFieldCreate] = Field(
        default_factory=list,
        description="List of form fields to create with the registration form",
    )


class RegistrationFormUpdate(BaseModel):
    fields: list[FormFieldCreate] | None = Field(
        None, description="List of form fields to update"
    )


class RegistrationFormResponse(RegistrationFormBase):
    id: int
    announcement_id: int
    fields: list[FormFieldResponse] = Field(
        default_factory=list,
        description="List of form fields in this registration form",
    )

    class Config:
        from_attributes = True
