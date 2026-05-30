from pydantic import BaseModel, ConfigDict, Field, computed_field

from datetime import datetime

from modules.games.schemas.responses import GameForAnnouncementResponse
from modules.participants.schemas.responses import AnnouncementParticipantResponse


class AnnouncementForRegistrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str | None
    format: str
    registration_end_at: datetime
    game: GameForAnnouncementResponse
    participants: list[AnnouncementParticipantResponse] = Field(
        default_factory=list, exclude=True
    )

    @computed_field
    @property
    def participants_count(self) -> int:
        """Number of confirmed participants in the announcement."""
        return len(self.participants)
