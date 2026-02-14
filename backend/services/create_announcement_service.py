from datetime import datetime, timezone
from models.user import User
from models.announcement import Announcement
from models.registration_form import RegistrationForm
from models.form_field import FormField
from schemas.announcement import AnnouncementCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from enums import AnnouncementStatus, SeedMethod


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

    def _determine_seed_method(self) -> SeedMethod:
        """
        Determine the seed method based on qualification settings.

        Returns:
            SeedMethod.QUALIFICATION_SCORE if has_qualification is True,
            SeedMethod.RANDOM otherwise.
        """
        if self.announcement_in.has_qualification:
            return SeedMethod.QUALIFICATION_SCORE

        return SeedMethod.RANDOM

    def _prepare_announcement(self, announcement: Announcement) -> None:
        """
        Prepare announcement by setting derived fields.

        Sets seed_method based on qualification settings,
        status based on current time, and organizer.
        """
        announcement.seed_method = self._determine_seed_method()

        now = datetime.now(timezone.utc)
        if announcement.registration_start_at <= now:
            announcement.status = AnnouncementStatus.REGISTRATION_OPEN
        else:
            announcement.status = AnnouncementStatus.PRE_REGISTRATION

        announcement.organizer = self.user

    async def _create_registration_form(self, announcement_id: int) -> None:
        """
        Create registration form with fields if provided.

        Creates a RegistrationForm and associated FormFields
        if registration_form data is present in the input.
        """
        registration_form_data = self.announcement_in.registration_form

        if not registration_form_data or not registration_form_data.fields:
            return

        registration_form = RegistrationForm(announcement_id=announcement_id)
        self.session.add(registration_form)
        await self.session.flush()

        for field_data in registration_form_data.fields:
            form_field = FormField(
                **field_data.model_dump(), form_id=registration_form.id
            )
            self.session.add(form_field)

    async def call(self) -> Announcement:
        """Create a new announcement with optional custom registration form."""

        announcement_data = self.announcement_in.model_dump(
            exclude={"registration_form"}
        )
        announcement = Announcement(**announcement_data)
        self._prepare_announcement(announcement)

        self.session.add(announcement)
        await self.session.flush()

        await self._create_registration_form(announcement.id)

        await self.session.commit()

        result = await self.session.execute(
            select(Announcement).where(Announcement.id == announcement.id)
        )
        return result.scalar_one()
