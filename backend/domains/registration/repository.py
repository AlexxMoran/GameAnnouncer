from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, noload

from domains.announcements.model import Announcement
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
    ) -> Optional[RegistrationRequest]:
        """Fetch a single registration request with announcement participants and user loaded."""
        result = await self.session.execute(
            select(RegistrationRequest)
            .options(
                selectinload(RegistrationRequest.announcement).selectinload(
                    Announcement.participants
                ),
                selectinload(RegistrationRequest.user),
            )
            .where(RegistrationRequest.id == registration_request_id)
        )
        return result.scalar_one_or_none()

    async def find_all_by_user_id(
        self, user_id: int, skip: int = 0, limit: int = 10
    ) -> tuple[list[RegistrationRequest], int]:
        """Get paginated registration requests for a user."""
        count_result = await self.session.execute(
            select(func.count())
            .select_from(RegistrationRequest)
            .where(RegistrationRequest.user_id == user_id)
        )
        total = count_result.scalar_one()

        data_result = await self.session.execute(
            select(RegistrationRequest)
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
            .where(RegistrationRequest.announcement_id == announcement_id)
            .offset(skip)
            .limit(limit)
            .order_by(RegistrationRequest.created_at.desc())
        )
        return list(data_result.scalars().all()), total

    async def find_by_user_and_announcement(
        self, user_id: int, announcement_id: int
    ) -> Optional[RegistrationRequest]:
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
    ) -> Optional[RegistrationRequest]:
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

    async def save(
        self, registration_request: RegistrationRequest
    ) -> RegistrationRequest:
        """Persist a registration request. Flushes but does not commit."""
        self.session.add(registration_request)
        await self.session.flush()
        await self.session.refresh(registration_request)
        return registration_request


class RegistrationFormRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_announcement_id(
        self, announcement_id: int
    ) -> Optional[RegistrationForm]:
        """Fetch the registration form for an announcement, without eagerly loading fields."""
        result = await self.session.execute(
            select(RegistrationForm)
            .options(noload(RegistrationForm.fields))
            .where(RegistrationForm.announcement_id == announcement_id)
        )
        return result.scalar_one_or_none()

    async def save(self, registration_form: RegistrationForm) -> RegistrationForm:
        """Persist a registration form. Flushes but does not commit."""
        self.session.add(registration_form)
        await self.session.flush()
        await self.session.refresh(registration_form)
        return registration_form

    async def delete(self, registration_form: RegistrationForm) -> None:
        """Delete a registration form. Flushes but does not commit."""
        await self.session.delete(registration_form)
        await self.session.flush()
