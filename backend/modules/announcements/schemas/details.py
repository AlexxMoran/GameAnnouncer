from modules.announcements.schemas.responses import AnnouncementResponse
from modules.registration.schemas.responses import (
    CurrentUserRegistrationRequestResponse,
)


class AnnouncementDetailResponse(AnnouncementResponse):
    my_active_registration_request: CurrentUserRegistrationRequestResponse | None = None
