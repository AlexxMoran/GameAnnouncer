from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domains.announcements.model import Announcement
from domains.registration.models import RegistrationRequest, RegistrationForm, FormField
from domains.registration.schemas import RegistrationFormCreate
from domains.registration.repository import RegistrationFormRepository
from domains.registration.services.lifecycle import RegistrationLifecycleService
from enums import AnnouncementStatus
from enums.registration_status import RegistrationStatus
from exceptions import ValidationException

ALLOWED_FORM_UPDATE_STATUSES = {
    AnnouncementStatus.PRE_REGISTRATION,
    AnnouncementStatus.REGISTRATION_OPEN,
}


class UpsertRegistrationFormService:
    """Service for creating or replacing a registration form for an announcement.

    When an existing form is present, all active registration requests are rejected
    via the lifecycle service before the form is deleted and recreated.

    Form updates are only allowed when the announcement is in PRE_REGISTRATION
    or REGISTRATION_OPEN status.
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
        """Replace the registration form, rejecting active requests if a form already exists."""
        self._validate_announcement_status()

        repo = RegistrationFormRepository(self.session)
        existing_form = await repo.find_by_announcement_id(self.announcement.id)

        if existing_form:
            await self._reject_active_requests()
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

    def _validate_announcement_status(self) -> None:
        """Ensure the announcement is in a status that allows form updates."""
        status = AnnouncementStatus(self.announcement.status)
        if status not in ALLOWED_FORM_UPDATE_STATUSES:
            raise ValidationException(
                f"Registration form can only be updated when announcement is in "
                f"PRE_REGISTRATION or REGISTRATION_OPEN status, "
                f"current status is {status.value}"
            )

    async def _reject_active_requests(self) -> None:
        """Reject all active registration requests due to form change.

        Uses batch_system_reject to bulk-delete participants and transition
        each request via the state machine.
        """
        result = await self.session.execute(
            select(RegistrationRequest).where(
                RegistrationRequest.announcement_id == self.announcement.id,
                RegistrationRequest.status.in_(
                    [RegistrationStatus.PENDING, RegistrationStatus.APPROVED]
                ),
            )
        )
        active_requests = list(result.scalars().all())
        await RegistrationLifecycleService.batch_system_reject(
            active_requests, self.announcement, self.session
        )
