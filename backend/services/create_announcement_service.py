from datetime import datetime, timezone
from models.user import User
from models.announcement import Announcement
from models.registration_form import RegistrationForm
from models.form_field import FormField
from schemas.announcement import AnnouncementCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from enums import AnnouncementStatus


class CreateAnnouncementService:
    """Service for creating announcements with optional registration forms."""

    def __init__(
        self,
        session: AsyncSession,
        announcement_in: AnnouncementCreate,
        user: User,
    ):
        self.session = session
        self.announcement_in = announcement_in
        self.user = user

    async def call(self) -> Announcement:
        """Create a new announcement with optional custom registration form."""

        registration_form_data = self.announcement_in.registration_form

        announcement_data = self.announcement_in.model_dump(
            exclude={"registration_form"}
        )
        announcement = Announcement(**announcement_data)

        now = datetime.now(timezone.utc)
        if announcement.registration_start_at <= now:
            announcement.status = AnnouncementStatus.REGISTRATION_OPEN
        else:
            announcement.status = AnnouncementStatus.PRE_REGISTRATION

        announcement.organizer = self.user

        self.session.add(announcement)
        await self.session.flush()

        if registration_form_data and registration_form_data.fields:
            registration_form = RegistrationForm(announcement_id=announcement.id)
            self.session.add(registration_form)
            await self.session.flush()

            for field_data in registration_form_data.fields:
                form_field = FormField(
                    **field_data.model_dump(), form_id=registration_form.id
                )
                self.session.add(form_field)

        await self.session.commit()

        result = await self.session.execute(
            select(Announcement).where(Announcement.id == announcement.id)
        )
        return result.scalar_one()
