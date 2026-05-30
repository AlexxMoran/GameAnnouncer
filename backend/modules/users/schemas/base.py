from pydantic import Field

_HEX_COLOR_PATTERN = r"^#[0-9A-Fa-f]{6}$"


class UserBaseFieldsMixin:
    first_name: str | None = None
    last_name: str | None = None
    nickname: str | None = None
    avatar_icon_id: int | None = None
    avatar_color: str | None = Field(default=None, pattern=_HEX_COLOR_PATTERN)
