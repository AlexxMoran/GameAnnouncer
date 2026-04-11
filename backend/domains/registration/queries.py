from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domains.registration.models import RegistrationRequest


class RegistrationRequestQueries:
    """Read-side database access for RegistrationRequest entities."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_id(
        self, registration_request_id: int
    ) -> RegistrationRequest | None:
        """Fetch a registration request with announcement and user loaded."""
        result = await self.session.execute(
            select(RegistrationRequest)
            .options(
                selectinload(RegistrationRequest.announcement),
                selectinload(RegistrationRequest.user),
            )
            .where(RegistrationRequest.id == registration_request_id)
        )
        return result.scalar_one_or_none()

    async def find_all_by_user_id(
        self, user_id: int, skip: int = 0, limit: int = 10
    ) -> tuple[list[RegistrationRequest], int]:
        """Get paginated registration requests for a user with announcement loaded."""
        count_result = await self.session.execute(
            select(func.count())
            .select_from(RegistrationRequest)
            .where(RegistrationRequest.user_id == user_id)
        )
        total = count_result.scalar_one()

        data_result = await self.session.execute(
            select(RegistrationRequest)
            .options(
                selectinload(RegistrationRequest.announcement),
                selectinload(RegistrationRequest.user),
            )
            .where(RegistrationRequest.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(RegistrationRequest.created_at.desc())
        )
        return list(data_result.scalars().all()), total

    async def find_all_by_announcement_id(
        self, announcement_id: int, skip: int = 0, limit: int = 10
    ) -> tuple[list[RegistrationRequest], int]:
        """Get paginated registration requests for an announcement."""
        count_result = await self.session.execute(
            select(func.count())
            .select_from(RegistrationRequest)
            .where(RegistrationRequest.announcement_id == announcement_id)
        )
        total = count_result.scalar_one()

        data_result = await self.session.execute(
            select(RegistrationRequest)
            .options(
                selectinload(RegistrationRequest.announcement),
                selectinload(RegistrationRequest.user),
            )
            .where(RegistrationRequest.announcement_id == announcement_id)
            .offset(skip)
            .limit(limit)
            .order_by(RegistrationRequest.created_at.desc())
        )
        return list(data_result.scalars().all()), total
