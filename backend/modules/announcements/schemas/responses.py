from __future__ import annotations

from datetime import datetime

from pydantic import ConfigDict, Field, computed_field

from core.schemas.base import BaseSchemaWithPermissions
from modules.announcements.schemas.base import AnnouncementBase
from modules.games.schemas.responses import GameForAnnouncementResponse
from modules.participants.schemas.responses import AnnouncementParticipantResponse
from modules.registration.schemas.forms.responses import (
    RegistrationFormResponse,
)


class AnnouncementResponse(AnnouncementBase, BaseSchemaWithPermissions):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    created_at: datetime
    updated_at: datetime
    end_at: datetime | None = Field(
        None, description="The end date and time of the announcement"
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
    game_id: int = Field(..., exclude=True)
    qualification_finished: bool = Field(
        False, description="Whether the qualification stage has been completed"
    )
    game: GameForAnnouncementResponse = Field(
        ..., description="The game associated with this announcement"
    )

    @computed_field
    @property
    def participants_count(self) -> int:
        """Number of confirmed participants in the announcement."""
        return len(self.participants)
