from pydantic import BaseModel, Field
from datetime import datetime
from schemas.base import BaseSchemaWithPermissions


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


class AnnouncementAvatarUpdate(BaseModel):
    image_url: str | None = Field(
        None, max_length=500, description="URL to the announcement's image"
    )


class AnnouncementResponse(AnnouncementBase, BaseSchemaWithPermissions):
    id: int
    created_at: datetime
    updated_at: datetime
    image_url: str | None = Field(
        None, max_length=500, description="URL to the announcement's image"
    )
    organizer_id: int = Field(
        ..., description="The ID of the user who organized the announcement"
    )
