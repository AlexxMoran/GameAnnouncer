from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from schemas.user import UserResponse


class AnnouncementParticipantBase(BaseModel):
    qualification_score: int | None = Field(
        None, description="Qualification score of the participant"
    )
    qualification_rank: int | None = Field(
        None, description="Qualification rank of the participant"
    )
    seed: int | None = Field(None, description="Tournament seed of the participant")
    is_qualified: bool = Field(
        False, description="Whether the participant is qualified"
    )


class AnnouncementParticipantUpdate(BaseModel):
    qualification_score: int | None = Field(
        None, description="Qualification score of the participant"
    )
    qualification_rank: int | None = Field(
        None, description="Qualification rank of the participant"
    )
    seed: int | None = Field(None, description="Tournament seed of the participant")
    is_qualified: bool | None = Field(
        None, description="Whether the participant is qualified"
    )


class AnnouncementParticipantResponse(AnnouncementParticipantBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    announcement_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: UserResponse | None = Field(None, description="User information")
