from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends

from models.announcement import Announcement
from schemas.user import UserResponse
from models.user import User
from services.avatar_uploader import AvatarUploader
from schemas.announcement import (
    AnnouncementCreate,
    AnnouncementResponse,
    AnnouncementUpdate,
    AnnouncementAvatarUpdate,
)
from core.deps import SessionDep
from api.v1.crud.announcement import announcement_crud

from core.users import current_user


router = APIRouter(prefix="/games/{game_id}/announcements", tags=["announcements"])


async def get_announcement_dependency(
    session: SessionDep,
    announcement_id: int,
) -> Announcement:
    announcement = await announcement_crud.get_by_id(
        session=session,
        announcement_id=announcement_id,
    )
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
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
        raise HTTPException(status_code=404, detail="Announcement not found")
    return announcement


@router.get("/", response_model=list[AnnouncementResponse])
async def get_announcements(
    session: SessionDep, game_id: int, skip: int = 0, limit: int = 10
):
    announcements = await announcement_crud.get_all_by_game_id(
        session=session, game_id=game_id, skip=skip, limit=limit
    )

    return announcements


@router.get("/{announcement_id}", response_model=AnnouncementResponse)
async def get_announcement(
    announcement: Announcement = Depends(get_announcement_dependency),
):
    return announcement


@router.get("/{announcement_id}/participants", response_model=list[UserResponse])
async def get_announcement_participants(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
):
    participants = await announcement_crud.get_participants_by_announcement_id(
        session=session, announcement=announcement
    )

    return participants


@router.post("/", response_model=AnnouncementCreate)
async def create_announcement(
    session: SessionDep,
    announcement: AnnouncementCreate,
    user: User = Depends(current_user),
):
    announcement = await announcement_crud.create(
        session=session, announcement_in=announcement, user=user
    )

    return announcement


@router.put("/{announcement_id}", response_model=AnnouncementUpdate)
async def update_announcement(
    session: SessionDep,
    announcement_in: AnnouncementUpdate,
    announcement: Announcement = Depends(get_announcement_for_edit_dependency),
):
    updated_announcement = await announcement_crud.update(
        session=session, announcement=announcement, announcement_in=announcement_in
    )

    return updated_announcement


@router.post("/{announcement_id}/upload_image", response_model=AnnouncementAvatarUpdate)
async def upload_announcement_image(
    session: SessionDep,
    file: UploadFile = File(...),
    announcement: Announcement = Depends(get_announcement_for_edit_dependency),
):
    image_url = await AvatarUploader.upload_avatar(
        object_type="announcement", object_id=announcement.id, file=file
    )

    announcement.image_url = image_url

    await session.commit()
    await session.refresh(announcement)

    return announcement
