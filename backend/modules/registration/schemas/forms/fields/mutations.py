from pydantic import BaseModel, Field

from enums import FormFieldType
from modules.registration.schemas.forms.fields.base import FormFieldBase


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
