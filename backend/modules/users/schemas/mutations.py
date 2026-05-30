from pydantic import field_validator

from fastapi_users import schemas
from modules.users.schemas.base import _HEX_COLOR_PATTERN, UserBaseFieldsMixin


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
