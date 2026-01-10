from exceptions import ValidationException
from models.announcement import Announcement
from models.user import User
from schemas.registration_request import RegistrationRequestCreate
from models.registration_request import RegistrationRequest
from sqlalchemy.ext.asyncio import AsyncSession


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

    async def call(self) -> RegistrationRequest:
        """Create a new registration request with validation."""

        if not self.announcement.is_registration_open:
            raise ValidationException(
                "Registration is currently closed for this announcement"
            )

        registration_request = RegistrationRequest(
            **self.registration_request_in.model_dump()
        )
        registration_request.user = self.user

        self.session.add(registration_request)
        await self.session.commit()
        await self.session.refresh(registration_request)

        return registration_request
