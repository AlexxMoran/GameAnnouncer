from fastapi import APIRouter, Depends

from core.schemas.base import PaginatedResponse
from domains.users.model import User
from core.deps import SessionDep
from core.users import current_user

from domains.announcements.queries import AnnouncementQueries
from domains.registration.search import RegistrationRequestSearch
from domains.announcements.schemas import AnnouncementResponse
from domains.registration.schemas import (
    RegistrationRequestFilter,
    RegistrationRequestResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me/organized_announcements",
    response_model=PaginatedResponse[AnnouncementResponse],
)
async def get_my_organized_announcements(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
    user: User = Depends(current_user),
) -> PaginatedResponse[AnnouncementResponse]:
    queries = AnnouncementQueries(session)
    announcements, total = await queries.find_all_by_organizer_id(
        user.id, skip=skip, limit=limit
    )
    return PaginatedResponse(
        data=announcements,
        skip=skip,
        limit=limit,
        filtered_count=total,
        total_count=total,
    )


@router.get(
    "/me/participated_announcements",
    response_model=PaginatedResponse[AnnouncementResponse],
)
async def get_my_participated_announcements(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
    user: User = Depends(current_user),
) -> PaginatedResponse[AnnouncementResponse]:
    queries = AnnouncementQueries(session)
    announcements, total = await queries.find_all_by_participant_id(
        user.id, skip=skip, limit=limit
    )
    return PaginatedResponse(
        data=announcements,
        skip=skip,
        limit=limit,
        filtered_count=total,
        total_count=total,
    )


@router.get(
    "/me/registration_requests",
    response_model=PaginatedResponse[RegistrationRequestResponse],
)
async def get_my_registration_requests(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
    filters: RegistrationRequestFilter = Depends(),
    user: User = Depends(current_user),
) -> PaginatedResponse[RegistrationRequestResponse]:
    search = RegistrationRequestSearch(
        session=session,
        filters=filters,
        scope=user,
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


@router.get(
    "/{user_id}/organized_announcements",
    response_model=PaginatedResponse[AnnouncementResponse],
)
async def get_user_organized_announcements(
    user_id: int,
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
) -> PaginatedResponse[AnnouncementResponse]:
    queries = AnnouncementQueries(session)
    announcements, total = await queries.find_all_by_organizer_id(
        user_id, skip=skip, limit=limit
    )
    return PaginatedResponse(
        data=announcements,
        skip=skip,
        limit=limit,
        filtered_count=total,
        total_count=total,
    )
