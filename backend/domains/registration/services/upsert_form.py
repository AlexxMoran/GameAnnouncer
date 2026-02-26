from sqlalchemy.ext.asyncio import AsyncSession

from domains.announcements.model import Announcement
from domains.registration.models import RegistrationRequest, RegistrationForm, FormField
from domains.registration.schemas import RegistrationFormCreate
from domains.registration.repository import RegistrationFormRepository
from enums.registration_status import RegistrationStatus
from sqlalchemy import select


class UpsertRegistrationFormService:
    """Service for creating or replacing a registration form for an announcement.

    When an existing form is present, all active registration requests are cancelled
    before the form is deleted and recreated.
    """

    def __init__(
        self,
        session: AsyncSession,
        announcement: Announcement,
        registration_form_in: RegistrationFormCreate,
    ) -> None:
        self.session = session
        self.announcement = announcement
        self.registration_form_in = registration_form_in

    async def call(self) -> RegistrationForm:
        """Replace the registration form, cancelling active requests if a form already exists."""
        repo = RegistrationFormRepository(self.session)
        existing_form = await repo.find_by_announcement_id(self.announcement.id)

        if existing_form:
            await self._cancel_active_requests()
            await repo.delete(existing_form)

        registration_form = RegistrationForm(announcement_id=self.announcement.id)
        self.session.add(registration_form)
        await self.session.flush()

        for field_data in self.registration_form_in.fields:
            form_field = FormField(
                **field_data.model_dump(), form_id=registration_form.id
            )
            self.session.add(form_field)

        return registration_form

    async def _cancel_active_requests(self) -> None:
        """Cancel all pending and approved registration requests for this announcement."""
        result = await self.session.execute(
            select(RegistrationRequest).where(
                RegistrationRequest.announcement_id == self.announcement.id,
                RegistrationRequest.status.in_(
                    [RegistrationStatus.PENDING, RegistrationStatus.APPROVED]
                ),
            )
        )
        cancellation_reason = (
            "Registration form has been updated by the organizer. "
            "Please submit a new registration request with the updated form."
        )
        for request in result.scalars().all():
            request.status = RegistrationStatus.CANCELLED
            request.cancellation_reason = cancellation_reason
