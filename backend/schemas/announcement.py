from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from schemas.base import BaseSchemaWithPermissions


class AnnouncementBase(BaseModel):
    title: str = Field(..., max_length=200, description="The title of the announcement")
    content: Optional[str] = Field(None, description="The content of the announcement")
    game_id: int = Field(
        ..., description="The ID of the game this announcement belongs to"
    )


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = Field(
        None, max_length=200, description="The title of the announcement"
    )
    content: Optional[str] = None


class AnnouncementAvatarUpdate(BaseModel):
    image_url: Optional[str] = Field(
        None, max_length=500, description="URL to the announcement's image"
    )


class AnnouncementResponse(AnnouncementBase, BaseSchemaWithPermissions):
    id: int
    created_at: datetime
    updated_at: datetime
    image_url: Optional[str] = Field(
        None, max_length=500, description="URL to the announcement's image"
    )
    organizer_id: int = Field(
        ..., description="The ID of the user who organized the announcement"
    )
