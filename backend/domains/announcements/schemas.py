from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator

from core.schemas.base import BaseSchemaWithPermissions
from core.search.base_filter import BaseFilter
from domains.participants.schemas import AnnouncementParticipantResponse
from domains.registration.schemas import (
    RegistrationFormCreate,
    RegistrationFormResponse,
)


class AnnouncementBase(BaseModel):
    title: str = Field(..., max_length=200, description="The title of the announcement")
    content: str | None = Field(None, description="The content of the announcement")
    format: str = Field(..., description="The format of the announcement")
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
    has_qualification: bool = Field(
        False, description="Whether this announcement has a qualification stage"
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
    bracket_size: int | None = Field(
        None, description="The size of the tournament bracket, if applicable"
    )
    seed_method: str = Field(
        ..., description="The method used for seeding participants"
    )
    qualification_finished: bool = Field(
        False, description="Whether the qualification stage has been completed"
    )

    @computed_field
    @property
    def participants_count(self) -> int:
        return len(self.participants)


class AnnouncementFilter(BaseFilter):
    game_id: int | None = None
    status: str | None = None
    q: str | None = Field(None, max_length=100)

    @field_validator("q")
    @classmethod
    def validate_search_query(cls, v: str | None) -> str | None:
        """Validate search query: trim whitespace and return None for empty strings."""
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        return v
