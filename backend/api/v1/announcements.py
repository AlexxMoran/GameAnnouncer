from fastapi import APIRouter, HTTPException, UploadFile, File, Depends

from models.user import User
from services.avatar_uploader import AvatarUploader
from schemas.announcement import (
    AnnouncementCreate,
    AnnouncementResponse,
    AnnouncementUpdate,
)
from core.deps import SessionDep
from api.v1.crud.announcement import announcement_crud

from core.users import current_user


router = APIRouter(prefix="/games/{game_id}/announcements", tags=["announcements"])


@router.get("/", response_model=list[AnnouncementResponse])
async def get_announcements(
    session: SessionDep, game_id: int, skip: int = 0, limit: int = 10
):
    announcements = await announcement_crud.get_all_by_game_id(
        session=session, game_id=game_id, skip=skip, limit=limit
    )

    return announcements


@router.get("/{announcement_id}", response_model=AnnouncementResponse)
async def get_announcement(session: SessionDep, announcement_id: int):
    announcement = await announcement_crud.get_by_id(
        session=session, announcement_id=announcement_id
    )

    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    return announcement


@router.post("/", response_model=AnnouncementCreate)
async def create_announcement(
    session: SessionDep,
    announcement: AnnouncementCreate,
    current_user: User = Depends(current_user),
):
    announcement = await announcement_crud.create(
        session=session, announcement_in=announcement, user=current_user
    )

    return announcement


@router.put("/{announcement_id}", response_model=AnnouncementUpdate)
async def update_announcement(
    session: SessionDep, announcement_id: int, announcement: AnnouncementUpdate
):
    announcement_object = await announcement_crud.get_by_id(
        session=session, announcement_id=announcement_id
    )

    if not announcement_object:
        raise HTTPException(status_code=404, detail="Announcement not found")

    announcement = await announcement_crud.update(
        session=session, announcement=announcement_object, announcement_in=announcement
    )

    return announcement


@router.post("/{announcement_id}/upload_image", response_model=AnnouncementUpdate)
async def upload_announcement_image(
    session: SessionDep, announcement_id: int, file: UploadFile = File(...)
):
    announcement = await announcement_crud.get_by_id(
        session=session, announcement_id=announcement_id
    )

    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    image_url = await AvatarUploader.upload_avatar(
        object_type="announcement", object_id=announcement_id, file=file
    )

    announcement.image_url = image_url

    await session.commit()
    await session.refresh(announcement)

    return announcement
