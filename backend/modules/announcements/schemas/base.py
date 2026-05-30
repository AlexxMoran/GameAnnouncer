from datetime import datetime

from pydantic import BaseModel, Field


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
