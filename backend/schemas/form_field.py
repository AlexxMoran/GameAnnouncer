from pydantic import BaseModel, ConfigDict, Field
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
    options: dict | None = Field(
        default=None,
        description="The options for fields like selects, dropdowns or multiple choice",
    )


class FormFieldCreate(FormFieldBase):
    pass


class FormFieldUpdate(BaseModel):
    field_type: FormFieldType | None = Field(
        None, description="The type of the form field (text, select, radio, etc.)"
    )
    label: str | None = Field(
        None, max_length=200, description="The label/question for the form field"
    )
    required: bool | None = Field(
        None, description="Whether this field is required or optional"
    )
    options: dict | None = Field(
        None,
        description="The options for fields like selects, dropdowns or multiple choice",
    )


class FormFieldResponse(FormFieldBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    form_id: int
