from fastapi import APIRouter, Depends, File, UploadFile

from core.deps import SessionDep
from core.permissions import authorize_action
from core.schemas.base import DataResponse
from core.services.avatar_uploader import upload_avatar
from core.users import current_user
from modules.announcements.model import Announcement
from modules.announcements.repository import AnnouncementRepository
from modules.announcements.schemas.responses import AnnouncementResponse
from modules.users.model import User

from .dependencies import get_announcement_dependency

router = APIRouter()


@router.post(
    "/{announcement_id}/upload_image", response_model=DataResponse[AnnouncementResponse]
)
async def upload_announcement_image(
    session: SessionDep,
    file: UploadFile = File(...),
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, announcement, "edit")
    image_url = await upload_avatar(
        object_type="announcement", object_id=announcement.id, file=file
    )
    announcement.image_url = image_url
    repo = AnnouncementRepository(session)
    announcement = await repo.save(announcement)
    await session.commit()
    return DataResponse(data=announcement)
