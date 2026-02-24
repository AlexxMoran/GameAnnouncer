from pydantic import BaseModel, ConfigDict, Field, computed_field
from .form_field import FormFieldResponse as FormFieldSchema


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
    form_field: FormFieldSchema

    @computed_field
    @property
    def label(self) -> str:
        """The question/label shown to the user (e.g. 'Nickname in Game')."""

        return self.form_field.label
