from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import noload

from domains.registration.models import (
    RegistrationRequest,
    RegistrationForm,
)
from enums.registration_status import RegistrationStatus


class RegistrationRequestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_user_and_announcement(
        self, user_id: int, announcement_id: int
    ) -> RegistrationRequest | None:
        """Find an active (pending or approved) request for a user and announcement."""
        result = await self.session.execute(
            select(RegistrationRequest).where(
                RegistrationRequest.user_id == user_id,
                RegistrationRequest.announcement_id == announcement_id,
                RegistrationRequest.status.in_(
                    [RegistrationStatus.PENDING, RegistrationStatus.APPROVED]
                ),
            )
        )
        return result.scalar_one_or_none()


class RegistrationFormRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_announcement_id(
        self, announcement_id: int
    ) -> RegistrationForm | None:
        """Fetch the registration form for an announcement, without eagerly loading fields."""
        result = await self.session.execute(
            select(RegistrationForm)
            .options(noload(RegistrationForm.fields))
            .where(RegistrationForm.announcement_id == announcement_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, registration_form: RegistrationForm) -> None:
        """Delete a registration form. Flushes but does not commit."""
        await self.session.delete(registration_form)
        await self.session.flush()
