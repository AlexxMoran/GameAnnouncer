from models.announcement import Announcement
from models.registration_form import RegistrationForm
from models.form_field import FormField
from models.registration_request import RegistrationRequest
from schemas.registration_form import RegistrationFormCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import noload
from enums.registration_status import RegistrationStatus


class UpsertRegistrationFormService:
    """Service for creating or updating registration forms with automatic cancellation of active requests."""

    def __init__(
        self,
        session: AsyncSession,
        announcement: Announcement,
        registration_form_in: RegistrationFormCreate,
    ):
        self.session = session
        self.announcement = announcement
        self.registration_form_in = registration_form_in

    async def call(self) -> RegistrationForm:
        """Create or update registration form, cancelling active registration requests if form exists."""

        existing_form_result = await self.session.execute(
            select(RegistrationForm)
            .options(noload(RegistrationForm.fields))
            .where(RegistrationForm.announcement_id == self.announcement.id)
        )
        existing_form = existing_form_result.scalar_one_or_none()

        if existing_form:
            await self._cancel_active_requests()

            await self.session.delete(existing_form)
            await self.session.flush()

        registration_form = RegistrationForm(announcement_id=self.announcement.id)
        self.session.add(registration_form)
        await self.session.flush()

        for field_data in self.registration_form_in.fields:
            form_field = FormField(
                **field_data.model_dump(), form_id=registration_form.id
            )
            self.session.add(form_field)

        await self.session.commit()
        await self.session.refresh(registration_form)

        return registration_form

    async def _cancel_active_requests(self) -> list[RegistrationRequest]:
        """Cancel all pending and approved registration requests for this announcement."""

        result = await self.session.execute(
            select(RegistrationRequest).where(
                RegistrationRequest.announcement_id == self.announcement.id,
                RegistrationRequest.status.in_(
                    [RegistrationStatus.PENDING, RegistrationStatus.APPROVED]
                ),
            )
        )

        active_requests = result.scalars().all()

        cancellation_reason = "Registration form has been updated by the organizer. Please submit a new registration request with the updated form."

        for request in active_requests:
            request.status = RegistrationStatus.CANCELLED
            request.cancellation_reason = cancellation_reason

        return list(active_requests)
