from enum import Enum as PyEnum
from typing import Type

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String, func, select


class BaseSearch:
    model: Type
    filter_schema: Type

    def __init__(self, session, filters):
        self.session = session
        self.filters = filters

    def base_query(self):
        query = select(self.model)

        return self.apply_filters(query)

    @staticmethod
    def _normalize_filter_value(value: object) -> object:
        if isinstance(value, PyEnum):
            return value.value
        return value

    def apply_filters(self, query):
        values = self.filters.model_dump(exclude_none=True)

        for field, value in values.items():
            if value is None:
                continue

            value = self._normalize_filter_value(value)

            handler = getattr(self, f"filter_by_{field}", None)

            if handler:
                query = handler(query, value)
            else:
                column = getattr(self.model, field, None)
                if column is not None:
                    if isinstance(column.type, SQLEnum):
                        query = query.where(column == value)
                    elif isinstance(column.type, String):
                        query = query.where(column.ilike(f"%{value}%"))
                    else:
                        query = query.where(column == value)

        return query

    async def results(self, skip: int = 0, limit: int = 10):
        query = self.base_query().offset(skip).limit(limit)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def filtered_count(self) -> int:
        filtered_subquery = self.base_query().subquery()

        count_query = select(func.count()).select_from(filtered_subquery)
        result = await self.session.execute(count_query)

        return result.scalar_one()

    async def total_count(self) -> int:
        """Return total count of all records without any filters applied."""
        count_query = select(func.count()).select_from(self.model)
        result = await self.session.execute(count_query)
        return result.scalar_one()
