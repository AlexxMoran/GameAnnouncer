from pydantic import BaseModel, Field
from datetime import datetime
from schemas.base import BaseSchemaWithPermissions
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
    pass


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
