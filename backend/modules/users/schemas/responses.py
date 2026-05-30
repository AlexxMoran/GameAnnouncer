from pydantic import BaseModel, ConfigDict, Field

from fastapi_users import schemas
from modules.users.schemas.base import UserBaseFieldsMixin


class UserBrief(BaseModel, UserBaseFieldsMixin):
    """Lightweight user representation for embedding in related resources."""

    model_config = ConfigDict(from_attributes=True)

    id: int


class UserResponse(schemas.BaseUser[int], UserBaseFieldsMixin):
    permissions: dict[str, dict[str, bool]] = Field(default_factory=dict)
