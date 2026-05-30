from pydantic import BaseModel, Field

from modules.registration.schemas.forms.field_responses.base import (
    FormFieldResponseBase,
)


class FormFieldResponseCreate(FormFieldResponseBase):
    pass


class FormFieldResponseUpdate(BaseModel):
    value: str | None = Field(None, description="The user's response to the form field")
