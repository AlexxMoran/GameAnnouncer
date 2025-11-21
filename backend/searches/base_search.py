from sqlalchemy import select, func
from typing import Type


class BaseSearch:
    model: Type
    filter_schema: Type

    def __init__(self, session, filters):
        self.session = session
        self.filters = filters

    def base_query(self):
        query = select(self.model)

        return self.apply_filters(query)

    def apply_filters(self, query):
        values = self.filters.model_dump(exclude_none=True)

        for field, value in values.items():
            if value is None:
                continue

            handler = getattr(self, f"filter_by_{field}", None)

            if handler:
                query = handler(query, value)
            else:
                column = getattr(self.model, field, None)
                if column is not None:
                    query = query.where(column == value)

        return query

    async def results(self, skip: int = 0, limit: int = 10):
        query = self.base_query().offset(skip).limit(limit)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def count(self):
        filtered_subquery = self.base_query().subquery()

        count_query = select(func.count()).select_from(filtered_subquery)
        result = await self.session.execute(count_query)

        return result.scalar_one()
