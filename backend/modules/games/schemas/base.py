from pydantic import BaseModel, Field, field_validator

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

_CATEGORIES_LOWER: frozenset[str] = frozenset(c.lower() for c in GAME_CATEGORIES)


class CategoryValidator:
    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str | None) -> str | None:
        if v is not None and v.lower() not in _CATEGORIES_LOWER:
            raise ValueError(f'Category must be one of: {", ".join(GAME_CATEGORIES)}')
        return v


class GameBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = None
    category: str
