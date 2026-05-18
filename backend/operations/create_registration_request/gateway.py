from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from exceptions import AppException, ValidationException
from modules.announcements.model import Announcement
from modules.registration.models import RegistrationForm
from modules.registration.models import FormFieldResponse, RegistrationRequest
from modules.registration.repository import RegistrationRequestRepository
from operations.create_registration_request.contract import (
    CreateRegistrationRequestContract,
)
from operations.create_registration_request.structures import (
    CreateRegistrationRequestDecision,
    CreateRegistrationRequestSnapshot,
    RegistrationFormFieldSnapshot,
)

ACTIVE_REQUEST_UNIQUE_INDEX = "ix_registration_requests_active_user_announcement"


class CreateRegistrationRequestGateway:
    """Translates between ORM state and registration request creation data."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def load(
        self,
        contract: CreateRegistrationRequestContract,
    ) -> CreateRegistrationRequestSnapshot:
        announcement = await self._load_announcement(
            contract.registration_request_in.announcement_id
        )
        existing = await RegistrationRequestRepository(
            self._session
        ).find_by_user_and_announcement(
            user_id=contract.user_id,
            announcement_id=announcement.id,
        )
        form_fields = (
            [
                RegistrationFormFieldSnapshot(
                    id=field.id,
                    label=field.label,
                    required=field.required,
                )
                for field in announcement.registration_form.fields
            ]
            if announcement.registration_form
            else []
        )

        return CreateRegistrationRequestSnapshot(
            announcement_id=announcement.id,
            user_id=contract.user_id,
            request_data=contract.registration_request_in.model_dump(
                exclude={"form_responses"}
            ),
            form_responses=contract.registration_request_in.form_responses,
            is_registration_open=announcement.is_registration_open,
            has_existing_active_request=existing is not None,
            form_fields=form_fields,
        )

    async def apply(
        self,
        decision: CreateRegistrationRequestDecision,
    ) -> RegistrationRequest:
        registration_request = RegistrationRequest(**decision.request_data)
        registration_request.user_id = decision.user_id

        try:
            async with self._session.begin_nested():
                self._session.add(registration_request)
                await self._session.flush()
        except IntegrityError as exc:
            if not self._is_active_request_conflict(exc):
                raise
            raise ValidationException(
                "Registration request already exists for this user and announcement"
            ) from exc

        for response_data in decision.form_responses:
            self._session.add(
                FormFieldResponse(
                    **response_data.model_dump(),
                    registration_request_id=registration_request.id,
                )
            )

        return registration_request

    @staticmethod
    def _is_active_request_conflict(exc: IntegrityError) -> bool:
        error_text = str(getattr(exc, "orig", exc))
        return ACTIVE_REQUEST_UNIQUE_INDEX in error_text

    async def _load_announcement(self, announcement_id: int) -> Announcement:
        result = await self._session.execute(
            select(Announcement)
            .options(
                selectinload(Announcement.registration_form).selectinload(
                    RegistrationForm.fields
                )
            )
            .where(Announcement.id == announcement_id)
        )
        announcement = result.scalar_one_or_none()
        if announcement is None:
            raise AppException("Announcement not found", status_code=404)
        return announcement
