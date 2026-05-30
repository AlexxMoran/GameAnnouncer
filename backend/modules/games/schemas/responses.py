from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from core.schemas.base import BaseSchemaWithPermissions
from modules.games.schemas.base import GameBase


class GameResponse(GameBase, BaseSchemaWithPermissions):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    image_url: str | None = Field(None, max_length=500)
    announcements_count: int | None = None


class GameForAnnouncementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    image_url: str | None = Field(None, max_length=500)
    category: str
