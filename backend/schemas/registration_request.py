from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from schemas.form_field_response import (
    FormFieldResponseCreate,
    FormFieldResponseResponse,
)


class RegistrationRequestBase(BaseModel):
    announcement_id: int = Field(..., description="The ID of the announcement")


class RegistrationRequestCreate(RegistrationRequestBase):
    form_responses: list[FormFieldResponseCreate] = Field(
        default_factory=list,
        description="Responses to custom registration form fields, if announcement has a registration form",
    )


class RegistrationRequestUpdate(BaseModel):
    status: Optional[str] = Field(
        None, description="The status of the registration request"
    )


class RegistrationRequestResponse(RegistrationRequestBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int = Field(
        ..., description="The ID of the user who made the registration request"
    )
    status: str = Field(..., description="The status of the registration request")
    cancellation_reason: str | None = Field(
        None, description="Reason for cancellation/decline of the registration request"
    )
    form_responses: list[FormFieldResponseResponse] = Field(
        default_factory=list,
        description="User's responses to custom registration form fields",
    )
    created_at: datetime
    updated_at: datetime
