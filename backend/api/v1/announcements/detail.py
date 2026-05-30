from fastapi import APIRouter, Depends

from core.deps import SessionDep
from core.permissions import authorize_action, get_permissions
from core.schemas.base import DataResponse
from core.users import current_user, current_user_or_none
from modules.announcements.model import Announcement
from modules.announcements.repository import AnnouncementRepository
from modules.announcements.schemas.details import AnnouncementDetailResponse
from modules.announcements.schemas.mutations import AnnouncementUpdate
from modules.announcements.schemas.responses import AnnouncementResponse
from modules.registration.repository import RegistrationRequestRepository
from modules.users.model import User
from operations.update_announcement.contract import UpdateAnnouncementContract
from operations.update_announcement.scenario import UpdateAnnouncementScenario

from .dependencies import get_announcement_dependency

router = APIRouter()


@router.get(
    "/{announcement_id}", response_model=DataResponse[AnnouncementDetailResponse]
)
async def get_announcement(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User | None = Depends(current_user_or_none),
) -> DataResponse[AnnouncementDetailResponse]:
    announcement.permissions = get_permissions(user, announcement)
    if user is not None:
        announcement.my_active_registration_request = (
            await RegistrationRequestRepository(session).find_by_user_and_announcement(
                user_id=user.id,
                announcement_id=announcement.id,
            )
        )
    return DataResponse(data=announcement)


@router.patch("/{announcement_id}", response_model=DataResponse[AnnouncementResponse])
async def update_announcement(
    session: SessionDep,
    announcement_in: AnnouncementUpdate,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, announcement, "edit")

    scenario = UpdateAnnouncementScenario(session)
    announcement = await scenario.run(
        UpdateAnnouncementContract(
            announcement_id=announcement.id,
            announcement_in=announcement_in,
        )
    )
    await session.commit()
    return DataResponse(data=announcement)


@router.delete("/{announcement_id}", response_model=DataResponse[str])
async def delete_announcement(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[str]:
    authorize_action(user, announcement, "delete")
    repo = AnnouncementRepository(session)
    await repo.delete(announcement)
    await session.commit()
    return DataResponse(data="Announcement deleted successfully")
