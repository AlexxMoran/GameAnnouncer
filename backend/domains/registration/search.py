from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.search.base_search import BaseSearch
from domains.announcements.model import Announcement
from domains.registration.models import RegistrationRequest
from domains.registration.schemas import RegistrationRequestFilter
from domains.users.model import User


class RegistrationRequestSearch(BaseSearch):
    model = RegistrationRequest
    filter_schema = RegistrationRequestFilter

    def __init__(
        self,
        session: AsyncSession,
        filters: RegistrationRequestFilter,
        scope: User | Announcement,
    ) -> None:
        if not isinstance(scope, (User, Announcement)):
            raise TypeError(f"Unsupported scope type: {type(scope)}")
        super().__init__(session=session, filters=filters)
        self.scope = scope

    def _scope_condition(self):
        if isinstance(self.scope, User):
            return RegistrationRequest.user_id == self.scope.id
        return RegistrationRequest.announcement_id == self.scope.id

    def base_query(self):
        query = (
            select(self.model)
            .options(
                selectinload(RegistrationRequest.announcement),
                selectinload(RegistrationRequest.user),
            )
            .where(self._scope_condition())
        )
        return self.apply_filters(query).order_by(desc(RegistrationRequest.created_at))

    async def total_count(self) -> int:
        """Return total count within scope, ignoring active filters."""
        scoped_subquery = select(self.model).where(self._scope_condition()).subquery()
        count_query = select(func.count()).select_from(scoped_subquery)
        result = await self.session.execute(count_query)
        return result.scalar_one()
