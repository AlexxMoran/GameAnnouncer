from pydantic import BaseModel, Field

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
