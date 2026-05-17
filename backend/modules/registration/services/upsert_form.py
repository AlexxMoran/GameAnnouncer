from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import set_committed_value

from modules.announcements.model import Announcement
from modules.registration.models import RegistrationForm, FormField
from modules.registration.form_schemas import RegistrationFormCreate
from modules.registration.repository import RegistrationFormRepository


class UpsertRegistrationFormService:
    """Create or replace a registration form for an announcement."""

    def __init__(
        self,
        session: AsyncSession,
        announcement: Announcement,
        registration_form_in: RegistrationFormCreate | None,
    ) -> None:
        self.session = session
        self.announcement = announcement
        self.registration_form_in = registration_form_in

    async def call(self) -> RegistrationForm | None:
        repo = RegistrationFormRepository(self.session)
        existing_form = await repo.find_by_announcement_id(self.announcement.id)

        if existing_form:
            await repo.delete(existing_form)

        if not self.registration_form_in or not self.registration_form_in.fields:
            set_committed_value(self.announcement, "registration_form", None)
            return None

        registration_form = RegistrationForm(announcement_id=self.announcement.id)
        self.session.add(registration_form)
        await self.session.flush()

        form_fields = []
        for field_data in self.registration_form_in.fields:
            form_field = FormField(
                **field_data.model_dump(), form_id=registration_form.id
            )
            self.session.add(form_field)
            form_fields.append(form_field)

        set_committed_value(registration_form, "fields", form_fields)
        set_committed_value(
            self.announcement,
            "registration_form",
            registration_form,
        )

        await self.session.flush()
        return registration_form
