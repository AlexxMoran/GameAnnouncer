from fastapi import APIRouter, Depends

from core.deps import SessionDep
from core.permissions import authorize_action
from core.schemas.base import PaginatedResponse
from core.users import current_user
from modules.announcements.model import Announcement
from modules.registration.schemas.filters import RegistrationRequestFilter
from modules.registration.schemas.responses import RegistrationRequestResponse
from modules.registration.search import RegistrationRequestSearch
from modules.users.model import User

from .dependencies import get_announcement_dependency

router = APIRouter()


@router.get(
    "/{announcement_id}/registration_requests",
    response_model=PaginatedResponse[RegistrationRequestResponse],
)
async def get_announcement_registration_requests(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
    filters: RegistrationRequestFilter = Depends(),
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> PaginatedResponse[RegistrationRequestResponse]:
    """
    List all registration requests for an announcement.

    Restricted to the announcement organizer and admins.
    Returns 401 if unauthenticated, 403 if authenticated but unauthorized.
    """
    authorize_action(user, announcement, "edit")
    search = RegistrationRequestSearch(
        session=session,
        filters=filters,
        scope=announcement,
    )
    registration_requests = await search.results(skip=skip, limit=limit)
    filtered_count = await search.filtered_count()
    total_count = await search.total_count()

    return PaginatedResponse(
        data=registration_requests,
        skip=skip,
        limit=limit,
        filtered_count=filtered_count,
        total_count=total_count,
    )
