from fastapi import APIRouter, Depends

from schemas.registration_request import RegistrationRequestResponse
from schemas.announcement import AnnouncementResponse
from schemas.base import DataResponse
from models.user import User

from core.deps import SessionDep
from api.v1.crud.announcement import announcement_crud
from api.v1.crud.registration_request import registration_request_crud

from core.users import current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me/organized_announcements",
    response_model=DataResponse[list[AnnouncementResponse]],
)
async def get_my_organized_announcements(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(current_user),
):
    announcements = await announcement_crud.get_all_by_organizer_id(
        session, current_user.id, skip=skip, limit=limit
    )

    return DataResponse(data=announcements)


@router.get(
    "/me/participated_announcements",
    response_model=DataResponse[list[AnnouncementResponse]],
)
async def get_my_participated_announcements(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(current_user),
):
    announcements = await announcement_crud.get_all_by_participant_id(
        session, current_user.id, skip=skip, limit=limit
    )

    return DataResponse(data=announcements)


@router.get(
    "/me/registation_requests",
    response_model=DataResponse[list[RegistrationRequestResponse]],
)
async def get_my_registration_requests(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(current_user),
):
    registration_requests = await registration_request_crud.get_all_by_user_id(
        session, current_user.id, skip=skip, limit=limit
    )

    return DataResponse(data=registration_requests)


@router.get(
    "/{user_id}/organized_announcements",
    response_model=DataResponse[list[AnnouncementResponse]],
)
async def get_user_organized_announcements(
    user_id: int,
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
):
    announcements = await announcement_crud.get_all_by_organizer_id(
        session, user_id, skip=skip, limit=limit
    )

    return DataResponse(data=announcements)
