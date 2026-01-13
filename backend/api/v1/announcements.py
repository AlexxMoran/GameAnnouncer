from fastapi import APIRouter, UploadFile, File, Depends
from exceptions import AppException

from schemas.registration_request import RegistrationRequestResponse
from models.announcement import Announcement
from schemas.user import UserResponse
from models.user import User
from services.avatar_uploader import upload_avatar
from schemas.announcement import (
    AnnouncementCreate,
    AnnouncementResponse,
    AnnouncementUpdate,
    AnnouncementStatusUpdate,
)
from schemas.base import PaginatedResponse, DataResponse
from schemas.filters.announcement_filter import AnnouncementFilter
from core.deps import SessionDep
from api.v1.crud.announcement import announcement_crud
from api.v1.crud.registration_request import registration_request_crud
from searches.announcement_search import AnnouncementSearch

from core.users import current_user, current_user_or_none
from core.permissions import get_permissions, get_batch_permissions


router = APIRouter(prefix="/announcements", tags=["announcements"])


async def get_announcement_dependency(
    session: SessionDep,
    announcement_id: int,
) -> Announcement:
    announcement = await announcement_crud.get_by_id(
        session=session,
        announcement_id=announcement_id,
    )
    if not announcement:
        raise AppException("Announcement not found", status_code=404)
    return announcement


async def get_announcement_for_edit_dependency(
    session: SessionDep,
    announcement_id: int,
    user: User = Depends(current_user),
) -> Announcement:
    announcement = await announcement_crud.get_by_id(
        session=session,
        announcement_id=announcement_id,
        user=user,
        action="edit",
    )
    if not announcement:
        raise AppException("Announcement not found", status_code=404)
    return announcement


@router.get("", response_model=PaginatedResponse[AnnouncementResponse])
async def get_announcements(
    session: SessionDep,
    filters: AnnouncementFilter = Depends(),
    user: User | None = Depends(current_user_or_none),
    skip: int = 0,
    limit: int = 10,
):
    search = AnnouncementSearch(session=session, filters=filters)
    announcements = await search.results(skip=skip, limit=limit)
    announcements_count = await search.count()

    get_batch_permissions(user, announcements)

    return PaginatedResponse(
        data=announcements, skip=skip, limit=limit, total=announcements_count
    )


@router.get("/{announcement_id}", response_model=DataResponse[AnnouncementResponse])
async def get_announcement(
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User | None = Depends(current_user_or_none),
):
    announcement.permissions = get_permissions(user, announcement)
    return DataResponse(data=announcement)


@router.get(
    "/{announcement_id}/participants", response_model=DataResponse[list[UserResponse]]
)
async def get_announcement_participants(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
):
    participants = await announcement_crud.get_participants_by_announcement_id(
        session=session, announcement=announcement
    )

    return DataResponse(data=participants)


@router.get(
    "/{announcement_id}/registration_requests",
    response_model=DataResponse[list[RegistrationRequestResponse]],
)
async def get_announcement_registration_requests(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
):
    registration_requests = await registration_request_crud.get_all_by_announcement_id(
        session=session, announcement_id=announcement.id
    )

    return DataResponse(data=registration_requests)


@router.post("", response_model=DataResponse[AnnouncementResponse], status_code=201)
async def create_announcement(
    session: SessionDep,
    announcement_in: AnnouncementCreate,
    user: User = Depends(current_user),
):
    announcement = await announcement_crud.create(
        session=session, announcement_in=announcement_in, user=user
    )

    return DataResponse(data=announcement)


@router.patch("/{announcement_id}", response_model=DataResponse[AnnouncementResponse])
async def update_announcement(
    session: SessionDep,
    announcement_in: AnnouncementUpdate,
    announcement: Announcement = Depends(get_announcement_for_edit_dependency),
    current_user: User = Depends(current_user),
):
    updated_announcement = await announcement_crud.update(
        session=session,
        announcement=announcement,
        announcement_in=announcement_in,
        user=current_user,
        action="edit",
    )

    return DataResponse(data=updated_announcement)


@router.delete("/{announcement_id}", response_model=DataResponse[str])
async def delete_announcement(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_for_edit_dependency),
    current_user: User = Depends(current_user),
):
    await announcement_crud.delete(
        session=session, announcement=announcement, user=current_user, action="delete"
    )

    return DataResponse(data="Announcement deleted successfully")


@router.patch(
    "/{announcement_id}/status", response_model=DataResponse[AnnouncementResponse]
)
async def update_status(
    session: SessionDep,
    announcement_in: AnnouncementStatusUpdate,
    announcement: Announcement = Depends(get_announcement_for_edit_dependency),
    current_user: User = Depends(current_user),
):
    updated_announcement = await announcement_crud.update_status(
        session=session,
        announcement=announcement,
        action=announcement_in.action,
        user=current_user,
    )

    return DataResponse(data=updated_announcement)


@router.post(
    "/{announcement_id}/upload_image", response_model=DataResponse[AnnouncementResponse]
)
async def upload_announcement_image(
    session: SessionDep,
    file: UploadFile = File(...),
    announcement: Announcement = Depends(get_announcement_for_edit_dependency),
):
    image_url = await upload_avatar(
        object_type="announcement", object_id=announcement.id, file=file
    )

    announcement.image_url = image_url

    await session.commit()
    await session.refresh(announcement)

    return DataResponse(data=announcement)
