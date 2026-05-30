from datetime import datetime

from pydantic import BaseModel, Field

from modules.announcements.schemas.base import AnnouncementBase
from modules.registration.schemas.forms.mutations import (
    RegistrationFormCreate,
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
    has_qualification: bool | None = Field(
        None, description="Whether this announcement has a qualification stage"
    )
    registration_form: RegistrationFormCreate | None = Field(
        None, description="Optional replacement registration form for this announcement"
    )


class AnnouncementAvatarUpdate(BaseModel):
    image_url: str | None = Field(
        None, max_length=500, description="URL to the announcement's image"
    )
