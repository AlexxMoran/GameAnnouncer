from pydantic import BaseModel, Field
from typing import TypeVar, Generic

T = TypeVar("T")


class BaseSchemaWithPermissions:
    permissions: dict[str, bool] = Field(default_factory=dict)


class DataResponse(BaseModel, Generic[T]):
    data: T


class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    skip: int
    limit: int
    total: int
