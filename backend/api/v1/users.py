from fastapi import APIRouter, HTTPException, UploadFile, File, Depends

from schemas.announcement import AnnouncementResponse
from models.user import User

from core.deps import SessionDep
from api.v1.crud.announcement import announcement_crud

from core.users import current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/organized_announcements", response_model=list[AnnouncementResponse])
async def get_my_organized_announcements(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(current_user),
):
    announcements = await announcement_crud.get_all_by_organizer_id(
        session, current_user.id, skip=skip, limit=limit
    )

    return announcements


@router.get("/me/participated_announcements", response_model=list[AnnouncementResponse])
async def get_my_participated_announcements(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(current_user),
):
    announcements = await announcement_crud.get_all_by_participant_id(
        session, current_user.id, skip=skip, limit=limit
    )

    return announcements


@router.get(
    "/{user_id}/organized_announcements", response_model=list[AnnouncementResponse]
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

    return announcements
