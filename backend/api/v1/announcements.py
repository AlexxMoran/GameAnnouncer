from fastapi import APIRouter, HTTPException

from schemas.announcement import AnnouncementCreate, AnnouncementResponse, AnnouncementUpdate
from core.deps import SessionDep
from api.v1.crud.announcement import announcement_crud


router = APIRouter(prefix="/games/{game_id}/announcements", tags=["announcements"])

@router.get("/", response_model=list[AnnouncementResponse])
async def get_announcements(session: SessionDep, game_id: int, skip: int = 0, limit: int = 10):
    announcements = await announcement_crud.get_all_by_game_id(session=session, game_id=game_id, skip=skip, limit=limit)

    return announcements

@router.get("/{announcement_id}", response_model=AnnouncementResponse)
async def get_announcement(session: SessionDep, announcement_id: int):
    announcement = await announcement_crud.get_by_id(session=session, announcement_id=announcement_id)

    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    return announcement

@router.post("/", response_model=AnnouncementCreate)
async def create_announcement(session: SessionDep, announcement: AnnouncementCreate):
    announcement = await announcement_crud.create(session=session, announcement_in=announcement)

    return announcement

@router.put("/{announcement_id}", response_model=AnnouncementUpdate)
async def update_announcement(session: SessionDep, announcement_id: int, announcement: AnnouncementUpdate):
    announcement_object = await announcement_crud.get_by_id(session=session, announcement_id=announcement_id)

    if not announcement_object:
        raise HTTPException(status_code=404, detail="Announcement not found")

    announcement = await announcement_crud.update(session=session, announcement=announcement_object, announcement_in=announcement)

    return announcement

