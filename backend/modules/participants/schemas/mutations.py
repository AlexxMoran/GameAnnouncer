from pydantic import BaseModel, Field


class AnnouncementParticipantScoreUpdate(BaseModel):
    qualification_score: int = Field(
        ..., gt=0, description="New qualification score for the participant"
    )
