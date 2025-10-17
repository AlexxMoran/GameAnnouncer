from typing import Optional

from fastapi_users import schemas


class UserBaseFieldsMixin:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    nickname: Optional[str] = None


class UserResponse(schemas.BaseUser[int], UserBaseFieldsMixin):
    pass


class UserCreate(schemas.BaseUserCreate, UserBaseFieldsMixin):
    pass


class UserUpdate(schemas.BaseUserUpdate, UserBaseFieldsMixin):
    pass
