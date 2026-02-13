from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, computed_field
from datetime import datetime
from schemas.base import BaseSchemaWithPermissions
from schemas.registration_form import RegistrationFormCreate, RegistrationFormResponse
from schemas.announcement_participant import AnnouncementParticipantResponse
from enum import Enum


class AnnouncementAction(str, Enum):
    FINISH = "finish"
    CANCEL = "cancel"


class AnnouncementBase(BaseModel):
    title: str = Field(..., max_length=200, description="The title of the announcement")
    content: str | None = Field(None, description="The content of the announcement")
    game_id: int = Field(
        ..., description="The ID of the game this announcement belongs to"
    )
    start_at: datetime = Field(
        ..., description="The start date and time of the announcement"
    )
    registration_start_at: datetime = Field(
        ..., description="The start date and time when registration begins"
    )
    registration_end_at: datetime = Field(
        ..., description="The end date and time when registration ends"
    )
    max_participants: int = Field(
        ..., gt=0, description="The maximum number of participants allowed"
    )


class AnnouncementCreate(AnnouncementBase):
    registration_form: RegistrationFormCreate | None = Field(
        None, description="Optional custom registration form for this announcement"
    )


class AnnouncementUpdate(BaseModel):
    title: str | None = Field(
        None, max_length=200, description="The title of the announcement"
    )
    content: str | None = None
    start_at: datetime | None = Field(
        None, description="The start date and time of the announcement"
    )
    registration_start_at: datetime | None = Field(
        None, description="The start date and time when registration begins"
    )
    registration_end_at: datetime | None = Field(
        None, description="The end date and time when registration ends"
    )
    max_participants: int | None = Field(
        None, gt=0, description="The maximum number of participants allowed"
    )


class AnnouncementAvatarUpdate(BaseModel):
    image_url: str | None = Field(
        None, max_length=500, description="URL to the announcement's image"
    )


class AnnouncementStatusUpdate(BaseModel):
    action: AnnouncementAction = Field(
        ..., description="Action to perform: 'finish' or 'cancel'"
    )


class AnnouncementResponse(AnnouncementBase, BaseSchemaWithPermissions):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    end_at: datetime | None = Field(
        None, description="The end date and time of the announcement"
    )
    image_url: str | None = Field(
        None, max_length=500, description="URL to the announcement's image"
    )
    organizer_id: int = Field(
        ..., description="The ID of the user who organized the announcement"
    )
    status: str = Field(..., description="The current status of the announcement")
    participants: list[AnnouncementParticipantResponse] = Field(
        default_factory=list,
        description="List of participants with their data",
        exclude=True,
    )
    registration_form: RegistrationFormResponse | None = Field(
        None, description="Custom registration form for this announcement, if exists"
    )

    @computed_field
    @property
    def participants_count(self) -> int:
        return len(self.participants)
