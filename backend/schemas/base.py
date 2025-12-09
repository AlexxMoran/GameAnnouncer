from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")


class DataResponse(BaseModel, Generic[T]):
    data: T


class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    skip: int
    limit: int
    total: int
