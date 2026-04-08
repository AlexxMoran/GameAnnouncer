from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from domains.registration.form_schemas import (
    FormFieldResponseCreate,
    FormFieldResponseResponse,
)
from domains.announcements.schemas import AnnouncementForRegistrationResponse
from domains.users.schemas import UserBrief


class RegistrationRequestBase(BaseModel):
    announcement_id: int = Field(..., description="The ID of the announcement")


class RegistrationRequestCreate(RegistrationRequestBase):
    form_responses: list[FormFieldResponseCreate] = Field(
        default_factory=list,
        description="Responses to custom registration form fields, if announcement has a registration form",
    )


class RegistrationRequestUpdate(BaseModel):
    status: str | None = Field(
        None, description="The status of the registration request"
    )


class RegistrationRequestResponse(RegistrationRequestBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int = Field(
        ..., description="The ID of the user who made the registration request"
    )
    user: UserBrief = Field(
        ..., description="Basic info of the user who made the registration request"
    )
    status: str = Field(..., description="The status of the registration request")
    cancellation_reason: str | None = Field(
        None, description="Reason for cancellation/decline of the registration request"
    )
    form_responses: list[FormFieldResponseResponse] = Field(
        default_factory=list,
        description="User's responses to custom registration form fields",
    )
    announcement: AnnouncementForRegistrationResponse = Field(
        ..., description="The announcement associated with this registration request"
    )
    created_at: datetime
    updated_at: datetime
