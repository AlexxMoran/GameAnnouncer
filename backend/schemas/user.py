from typing import Optional
from pydantic import Field

from fastapi_users import schemas


class UserBaseFieldsMixin:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    nickname: Optional[str] = None


class UserResponse(schemas.BaseUser[int], UserBaseFieldsMixin):
    global_permissions: dict[str, dict[str, bool]] = Field(default_factory=dict)


class UserCreate(schemas.BaseUserCreate, UserBaseFieldsMixin):
    pass


class UserUpdate(schemas.BaseUserUpdate, UserBaseFieldsMixin):
    pass
