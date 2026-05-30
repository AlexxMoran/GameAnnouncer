from pydantic import Field

from modules.games.schemas.base import CategoryValidator, GameBase


class GameCreate(GameBase, CategoryValidator):
    pass


class GameUpdate(GameBase, CategoryValidator):
    name: str | None = Field(None, max_length=100)
    description: str | None = None
    category: str | None = None
