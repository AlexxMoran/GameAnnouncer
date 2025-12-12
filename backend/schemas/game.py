from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

from schemas.base import BaseSchemaWithPermissions

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
    def validate_category(cls, v):
        if v.lower() not in {c.lower() for c in GAME_CATEGORIES}:
            raise ValueError(f'Category must be one of: {", ".join(GAME_CATEGORIES)}')
        return v


class GameBase(BaseModel):
    name: str = Field(..., max_length=100, description="The name of the game")
    description: Optional[str] = Field(
        None, description="A brief description of the game"
    )
    category: str = Field(..., description="The category of the game")


class GameCreate(GameBase, CategoryValidator):
    pass


class GameUpdate(GameBase, CategoryValidator):
    name: Optional[str] = Field(
        None, max_length=100, description="The name of the game"
    )
    description: Optional[str] = None
    category: Optional[str] = Field(None, description="The category of the game")


class GameResponse(GameBase, BaseSchemaWithPermissions):
    id: int
    created_at: datetime
    updated_at: datetime
    image_url: Optional[str] = Field(
        None, max_length=500, description="URL to the game's image"
    )
    announcements_count: Optional[int] = Field(
        None, description="Number of announcements for this game"
    )


class GameAvatarUpdate(BaseModel):
    image_url: Optional[str] = Field(
        None, max_length=500, description="URL to the game's image"
    )
