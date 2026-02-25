from pydantic import Field

from fastapi_users import schemas


class UserBaseFieldsMixin:
    first_name: str | None = None
    last_name: str | None = None
    nickname: str | None = None


class UserResponse(schemas.BaseUser[int], UserBaseFieldsMixin):
    permissions: dict[str, dict[str, bool]] = Field(default_factory=dict)


class UserCreate(schemas.BaseUserCreate, UserBaseFieldsMixin):
    pass


class UserUpdate(schemas.BaseUserUpdate, UserBaseFieldsMixin):
    pass
