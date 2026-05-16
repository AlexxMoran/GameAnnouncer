from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, computed_field

from enums import FormFieldType


class FormFieldBase(BaseModel):
    field_type: FormFieldType = Field(
        ..., description="The type of the form field (text, select, radio, etc.)"
    )
    label: str = Field(
        ..., max_length=200, description="The label/question for the form field"
    )
    required: bool = Field(
        default=False, description="Whether this field is required or optional"
    )
    options: list[str] | None = Field(
        default=None,
        description="The options for fields like selects, dropdowns or multiple choice",
    )


class FormFieldCreate(FormFieldBase):
    pass


class FormFieldUpdate(BaseModel):
    field_type: FormFieldType | None = Field(
        None, description="The type of the form field"
    )
    label: str | None = Field(
        None, max_length=200, description="The label/question for the form field"
    )
    required: bool | None = Field(
        None, description="Whether this field is required or optional"
    )
    options: list[str] | None = Field(
        None, description="The options for select-type fields"
    )


class FormFieldResponse(FormFieldBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    form_id: int


class FormFieldResponseBase(BaseModel):
    form_field_id: int = Field(
        ..., description="The ID of the form field being answered"
    )
    value: str = Field(..., description="The user's response to the form field")


class FormFieldResponseCreate(FormFieldResponseBase):
    pass


class FormFieldResponseUpdate(BaseModel):
    value: str | None = Field(None, description="The user's response to the form field")


class FormFieldResponseResponse(FormFieldResponseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    registration_request_id: int
    form_field: FormFieldResponse | None = None

    @computed_field
    @property
    def label(self) -> str | None:
        """The question/label shown to the user (e.g. 'Nickname in Game')."""
        return self.form_field.label if self.form_field else None


class RegistrationFormCreate(BaseModel):
    fields: list[FormFieldCreate] = Field(
        default_factory=list,
        description="List of form fields to create with the registration form",
    )


class RegistrationFormUpdate(BaseModel):
    fields: list[FormFieldCreate] | None = Field(
        None, description="List of form fields to update"
    )


class RegistrationFormResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    announcement_id: int
    fields: list[FormFieldResponse] = Field(
        default_factory=list,
        description="List of form fields in this registration form",
    )
