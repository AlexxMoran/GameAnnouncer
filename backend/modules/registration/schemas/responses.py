from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from modules.announcements.schemas.summaries import AnnouncementForRegistrationResponse
from modules.registration.schemas.base import RegistrationRequestBase
from modules.registration.schemas.forms.field_responses.responses import (
    FormFieldResponseResponse,
)
from modules.users.schemas.responses import UserBrief


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


class CurrentUserRegistrationRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str = Field(..., description="The status of the registration request")
