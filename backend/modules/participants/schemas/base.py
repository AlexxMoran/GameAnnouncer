from pydantic import BaseModel, Field


class AnnouncementParticipantBase(BaseModel):
    qualification_score: int | None = Field(
        None, description="Qualification score of the participant"
    )
    qualification_rank: int | None = Field(
        None, description="Qualification rank of the participant"
    )
    seed: int | None = Field(None, description="Tournament seed of the participant")
    placement: int | None = Field(None, description="Final tournament placement")
    is_qualified: bool = Field(
        False, description="Whether the participant is qualified"
    )
