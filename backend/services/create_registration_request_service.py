from exceptions import ValidationException
from models.announcement import Announcement
from models.user import User
from models.form_field_response import FormFieldResponse
from models.registration_form import RegistrationForm
from schemas.registration_request import RegistrationRequestCreate
from schemas.form_field_response import FormFieldResponseCreate
from models.registration_request import RegistrationRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class CreateRegistrationRequestService:
    """Service for creating registration requests with business logic validation."""

    def __init__(
        self,
        session: AsyncSession,
        announcement: Announcement,
        user: User,
        registration_request_in: RegistrationRequestCreate,
    ):
        self.session = session
        self.announcement = announcement
        self.user = user
        self.registration_request_in = registration_request_in

    @property
    def registration_form(self) -> RegistrationForm | None:
        """Get registration form from announcement."""
        return self.announcement.registration_form

    @property
    def form_responses_data(self) -> list[FormFieldResponseCreate]:
        """Get form responses from input."""
        return self.registration_request_in.form_responses

    async def call(self) -> RegistrationRequest:
        """
        Create a new registration request with validation.

        If announcement has a registration form, validates that all required
        fields are filled and creates form field responses.
        """
        self._validate_registration()

        registration_request = await self._create_registration_request()
        self._create_form_responses_if_needed(registration_request)

        await self.session.commit()

        return await self._reload_request(registration_request.id)

    def _validate_registration(self) -> None:
        """
        Validate that registration is possible.

        Raises:
            ValidationException: If registration is closed or form responses are invalid
        """
        if not self.announcement.is_registration_open:
            raise ValidationException(
                "Registration is currently closed for this announcement"
            )

        if not self.registration_form and self.form_responses_data:
            raise ValidationException(
                "This announcement does not have a registration form. No form responses are required."
            )

        if self.registration_form:
            self._validate_form_responses(
                self.registration_form, self.form_responses_data
            )

    async def _create_registration_request(self) -> RegistrationRequest:
        """
        Create the registration request object.

        Returns:
            Created RegistrationRequest (not yet committed)
        """
        registration_request_data = self.registration_request_in.model_dump(
            exclude={"form_responses"}
        )
        registration_request = RegistrationRequest(**registration_request_data)
        registration_request.user = self.user

        self.session.add(registration_request)
        await self.session.flush()

        return registration_request

    def _create_form_responses_if_needed(
        self, registration_request: RegistrationRequest
    ) -> None:
        """
        Create form field responses if announcement has a registration form.

        Args:
            registration_request: The registration request to attach responses to
        """
        if not self.registration_form or not self.form_responses_data:
            return

        for response_data in self.form_responses_data:
            form_response = FormFieldResponse(
                **response_data.model_dump(),
                registration_request_id=registration_request.id,
            )
            self.session.add(form_response)

    async def _reload_request(self, request_id: int) -> RegistrationRequest:
        """
        Reload registration request from database with all relationships.

        Args:
            request_id: ID of the registration request to reload

        Returns:
            Reloaded RegistrationRequest with all relationships loaded
        """
        result = await self.session.execute(
            select(RegistrationRequest)
            .options(
                selectinload(RegistrationRequest.form_responses).selectinload(
                    FormFieldResponse.form_field
                )
            )
            .where(RegistrationRequest.id == request_id)
        )
        return result.scalar_one()

    def _validate_form_responses(
        self,
        registration_form: RegistrationForm,
        form_responses_data: list[FormFieldResponseCreate],
    ) -> None:
        """
        Validate form responses against registration form.

        Checks:
        1. All required fields are filled
        2. All provided form_field_ids belong to this registration form

        Args:
            registration_form: The registration form to validate against
            form_responses_data: User's responses to validate

        Raises:
            ValidationException: If validation fails
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
                f"Invalid form field IDs: {invalid_field_ids}. These fields do not belong to this announcement's registration form."
            )

        missing_required_fields = required_field_ids - provided_field_ids
        if missing_required_fields:
            missing_labels = [
                field.label for field in fields if field.id in missing_required_fields
            ]
            raise ValidationException(
                f"Missing required fields: {', '.join(missing_labels)}"
            )
