from pydantic import BaseModel, Field, field_validator
from typing import Optional
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
    description: Optional[str] = None
    category: str


class GameCreate(GameBase, CategoryValidator):
    pass


class GameUpdate(GameBase, CategoryValidator):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = None


class GameResponse(GameBase, BaseSchemaWithPermissions):
    id: int
    created_at: datetime
    updated_at: datetime
    image_url: Optional[str] = Field(None, max_length=500)
    announcements_count: Optional[int] = None

    model_config = {"from_attributes": True}


class GameFilter(BaseFilter):
    name: str | None = None
