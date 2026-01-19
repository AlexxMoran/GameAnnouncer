from pydantic import BaseModel, Field


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
    id: int
    registration_request_id: int

    class Config:
        from_attributes = True
