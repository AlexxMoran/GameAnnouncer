from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from domains.announcements.model import Announcement
from domains.registration.models import (
    RegistrationRequest,
    FormFieldResponse,
    RegistrationForm,
)
from domains.registration.schemas import RegistrationRequestCreate
from domains.registration.form_schemas import FormFieldResponseCreate
from domains.registration.repository import RegistrationRequestRepository
from domains.users.model import User
from exceptions import ValidationException

ACTIVE_REQUEST_UNIQUE_INDEX = "ix_registration_requests_active_user_announcement"


class CreateRegistrationRequestService:
    """Service for creating registration requests with business logic validation."""

    def __init__(
        self,
        session: AsyncSession,
        announcement: Announcement,
        user: User,
        registration_request_in: RegistrationRequestCreate,
    ) -> None:
        self.session = session
        self.announcement = announcement
        self.user = user
        self.registration_request_in = registration_request_in

    @property
    def _registration_form(self) -> RegistrationForm | None:
        """Get registration form from announcement."""
        return self.announcement.registration_form

    @property
    def _form_responses_data(self) -> list[FormFieldResponseCreate]:
        """Get form responses from input."""
        return self.registration_request_in.form_responses

    async def call(self) -> RegistrationRequest:
        """
        Create a new registration request with validation.

        Validates registration window and form responses, creates the request
        (and optional form field responses), and returns fully loaded result.
        """
        await self._validate_registration()

        registration_request = await self._create_registration_request()
        self._create_form_responses_if_needed(registration_request)
        return registration_request

    async def _validate_registration(self) -> None:
        """
        Validate that registration is allowed.

        Checks: registration window is open, no active request already exists,
        form responses are valid when a registration form is present.
        """
        if not self.announcement.is_registration_open:
            raise ValidationException(
                "Registration is currently closed for this announcement"
            )

        repo = RegistrationRequestRepository(self.session)
        existing = await repo.find_by_user_and_announcement(
            user_id=self.user.id,
            announcement_id=self.announcement.id,
        )
        if existing:
            raise ValidationException(
                "Registration request already exists for this user and announcement"
            )

        if not self._registration_form and self._form_responses_data:
            raise ValidationException(
                "This announcement does not have a registration form. No form responses are required."
            )

        if self._registration_form:
            self._validate_form_responses(
                self._registration_form, self._form_responses_data
            )

    async def _create_registration_request(self) -> RegistrationRequest:
        """Create and flush the registration request object.

        If a concurrent request has already created an active registration
        (race condition), the partial unique index will raise an IntegrityError
        which is converted to a user-friendly ValidationException.
        """
        registration_request_data = self.registration_request_in.model_dump(
            exclude={"form_responses"}
        )
        registration_request = RegistrationRequest(**registration_request_data)
        registration_request.user_id = self.user.id

        try:
            async with self.session.begin_nested():
                self.session.add(registration_request)
                await self.session.flush()
        except IntegrityError as exc:
            if not self._is_active_request_conflict(exc):
                raise
            raise ValidationException(
                "Registration request already exists for this user and announcement"
            ) from exc

        return registration_request

    @staticmethod
    def _is_active_request_conflict(exc: IntegrityError) -> bool:
        """Return True only for the partial unique index enforcing active requests."""
        error_text = str(getattr(exc, "orig", exc))
        return ACTIVE_REQUEST_UNIQUE_INDEX in error_text

    def _create_form_responses_if_needed(
        self, registration_request: RegistrationRequest
    ) -> None:
        """Add form field response objects to the session if applicable."""
        if not self._registration_form or not self._form_responses_data:
            return

        for response_data in self._form_responses_data:
            form_response = FormFieldResponse(
                **response_data.model_dump(),
                registration_request_id=registration_request.id,
            )
            self.session.add(form_response)

    def _validate_form_responses(
        self,
        registration_form: RegistrationForm,
        form_responses_data: list[FormFieldResponseCreate],
    ) -> None:
        """
        Validate form responses against the registration form.

        Ensures all required fields are answered and all provided field IDs
        belong to this form.
        """
        fields = registration_form.fields
        field_ids = {field.id for field in fields}
        required_field_ids = {field.id for field in fields if field.required}
        provided_field_ids = {
            response.form_field_id for response in form_responses_data
        }

        invalid_field_ids = provided_field_ids - field_ids
        if invalid_field_ids:
            raise ValidationException(
                f"Invalid form field IDs: {invalid_field_ids}. "
                "These fields do not belong to this announcement's registration form."
            )

        missing_required_fields = required_field_ids - provided_field_ids
        if missing_required_fields:
            missing_labels = [
                field.label for field in fields if field.id in missing_required_fields
            ]
            raise ValidationException(
                f"Missing required fields: {', '.join(missing_labels)}"
            )
