from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GameBase(BaseModel):
    name: str = Field(..., max_length=100, description="The name of the game")
    description: Optional[str] = Field(
        None, description="A brief description of the game"
    )
    image_url: Optional[str] = Field(
        None, max_length=500, description="URL to the game's image"
    )


class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    name: Optional[str] = Field(
        None, max_length=100, description="The name of the game"
    )
    description: Optional[str] = None


class GameResponse(GameBase):
    id: int
    created_at: datetime
    updated_at: datetime


class GameListResponse(BaseModel):
    games: list[GameResponse]
    count: int
