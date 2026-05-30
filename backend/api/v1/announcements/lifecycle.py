from fastapi import APIRouter, Depends

from core.deps import SessionDep
from core.permissions import authorize_action
from core.schemas.base import DataResponse
from core.users import current_user
from modules.announcements.model import Announcement
from modules.announcements.schemas.responses import AnnouncementResponse
from modules.announcements.services.lifecycle import AnnouncementLifecycleService
from modules.users.model import User
from operations.finalize_announcement_qualification.contract import (
    FinalizeAnnouncementQualificationContract,
)
from operations.finalize_announcement_qualification.scenario import (
    FinalizeAnnouncementQualificationScenario,
)
from operations.generate_announcement_bracket.contract import (
    GenerateAnnouncementBracketContract,
)
from operations.generate_announcement_bracket.scenario import (
    GenerateAnnouncementBracketScenario,
)

from .dependencies import get_announcement_dependency

router = APIRouter()


@router.post(
    "/{announcement_id}/open_registration",
    response_model=DataResponse[AnnouncementResponse],
)
async def open_registration(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, announcement, "manage_lifecycle")
    service = AnnouncementLifecycleService(announcement, session)
    announcement = await service.open_registration()
    await session.commit()
    return DataResponse(data=announcement)


@router.post(
    "/{announcement_id}/close_registration",
    response_model=DataResponse[AnnouncementResponse],
)
async def close_registration(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, announcement, "manage_lifecycle")
    service = AnnouncementLifecycleService(announcement, session)
    announcement = await service.close_registration()
    await session.commit()
    return DataResponse(data=announcement)


@router.post(
    "/{announcement_id}/start_qualification",
    response_model=DataResponse[AnnouncementResponse],
)
async def start_qualification(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, announcement, "manage_lifecycle")
    service = AnnouncementLifecycleService(announcement, session)
    announcement = await service.start_qualification()
    await session.commit()
    return DataResponse(data=announcement)


@router.post(
    "/{announcement_id}/finalize_qualification",
    response_model=DataResponse[AnnouncementResponse],
)
async def finalize_qualification(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, announcement, "manage_lifecycle")
    scenario = FinalizeAnnouncementQualificationScenario(session)
    announcement = await scenario.run(
        FinalizeAnnouncementQualificationContract(announcement_id=announcement.id)
    )
    await session.commit()
    return DataResponse(data=announcement)


@router.post(
    "/{announcement_id}/generate_bracket",
    response_model=DataResponse[AnnouncementResponse],
)
async def generate_bracket(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, announcement, "manage_lifecycle")
    scenario = GenerateAnnouncementBracketScenario(session)
    announcement = await scenario.run(
        GenerateAnnouncementBracketContract(announcement_id=announcement.id)
    )
    await session.commit()
    return DataResponse(data=announcement)


@router.post(
    "/{announcement_id}/cancel",
    response_model=DataResponse[AnnouncementResponse],
)
async def cancel_announcement(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, announcement, "manage_lifecycle")
    service = AnnouncementLifecycleService(announcement, session)
    announcement = await service.cancel()
    await session.commit()
    return DataResponse(data=announcement)
