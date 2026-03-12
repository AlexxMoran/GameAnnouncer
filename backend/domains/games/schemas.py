from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

from core.schemas.base import BaseSchemaWithPermissions
from core.search.base_filter import BaseFilter

GAME_CATEGORIES = [
    "RTS",
    "TBS",
    "MOBA",
    "FPS",
    "TPS",
    "Fighting",
    "Racing",
    "Sports",
    "Card",
    "Battle Royale",
    "Rhythm",
    "Party",
    "Simulation",
]


class CategoryValidator:
    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        if v.lower() not in {c.lower() for c in GAME_CATEGORIES}:
            raise ValueError(f'Category must be one of: {", ".join(GAME_CATEGORIES)}')
        return v


class GameBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = None
    category: str


class GameCreate(GameBase, CategoryValidator):
    pass


class GameUpdate(GameBase, CategoryValidator):
    name: str | None = Field(None, max_length=100)
    description: str | None = None
    category: str | None = None


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


class GameFilter(BaseFilter):
    name: str | None = None
