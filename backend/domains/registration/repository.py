from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, noload

from domains.registration.models import (
    RegistrationRequest,
    RegistrationForm,
    FormFieldResponse,
)
from enums.registration_status import RegistrationStatus


class RegistrationRequestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_id(
        self, registration_request_id: int
    ) -> RegistrationRequest | None:
        """Fetch a registration request with announcement and user loaded.

        Announcement sub-relationships (game, participants, registration_form)
        are loaded automatically via lazy='selectin' on the Announcement model.
        """
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
            .options(selectinload(RegistrationRequest.announcement))
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
            .options(selectinload(RegistrationRequest.announcement))
            .where(RegistrationRequest.announcement_id == announcement_id)
            .offset(skip)
            .limit(limit)
            .order_by(RegistrationRequest.created_at.desc())
        )
        return list(data_result.scalars().all()), total

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

    async def find_by_id_with_form_responses(
        self, registration_request_id: int
    ) -> RegistrationRequest | None:
        """Fetch a registration request with form_responses and form_field loaded."""
        result = await self.session.execute(
            select(RegistrationRequest)
            .options(
                selectinload(RegistrationRequest.form_responses).selectinload(
                    FormFieldResponse.form_field
                )
            )
            .where(RegistrationRequest.id == registration_request_id)
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
