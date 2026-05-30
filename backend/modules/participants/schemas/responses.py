from __future__ import annotations

from datetime import datetime

from pydantic import ConfigDict, Field

from modules.participants.schemas.base import AnnouncementParticipantBase
from modules.users.schemas.responses import UserResponse


class AnnouncementParticipantResponse(AnnouncementParticipantBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    announcement_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: UserResponse | None = Field(None, description="User information")
