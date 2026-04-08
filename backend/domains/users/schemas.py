from pydantic import BaseModel, ConfigDict, Field, field_validator

from fastapi_users import schemas

_HEX_COLOR_PATTERN = r"^#[0-9A-Fa-f]{6}$"


class UserBaseFieldsMixin:
    first_name: str | None = None
    last_name: str | None = None
    nickname: str | None = None
    avatar_icon_id: int | None = None
    avatar_color: str | None = Field(default=None, pattern=_HEX_COLOR_PATTERN)


class UserBrief(BaseModel, UserBaseFieldsMixin):
    """Lightweight user representation for embedding in related resources."""

    model_config = ConfigDict(from_attributes=True)

    id: int


class UserResponse(schemas.BaseUser[int], UserBaseFieldsMixin):
    permissions: dict[str, dict[str, bool]] = Field(default_factory=dict)


class UserCreate(schemas.BaseUserCreate, UserBaseFieldsMixin):
    pass


class UserUpdate(schemas.BaseUserUpdate, UserBaseFieldsMixin):
    @field_validator("avatar_color", mode="before")
    @classmethod
    def validate_avatar_color(cls, v: str | None) -> str | None:
        """Ensure avatar_color is a valid HEX color or None."""
        import re

        if v is not None and not re.fullmatch(_HEX_COLOR_PATTERN, v):
            raise ValueError("avatar_color must be a valid HEX color, e.g. '#FF5733'")
        return v
