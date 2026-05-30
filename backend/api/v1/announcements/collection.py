from fastapi import APIRouter, Depends

from core.deps import SessionDep
from core.permissions import authorize_action, get_batch_permissions
from core.schemas.base import DataResponse, PaginatedResponse
from core.users import current_user, current_user_or_none
from modules.announcements.model import Announcement
from modules.announcements.search import AnnouncementSearch
from modules.announcements.schemas.filters import AnnouncementFilter
from modules.announcements.schemas.mutations import AnnouncementCreate
from modules.announcements.schemas.responses import AnnouncementResponse
from modules.users.model import User
from operations.create_announcement.contract import CreateAnnouncementContract
from operations.create_announcement.scenario import CreateAnnouncementScenario

router = APIRouter()


@router.get("", response_model=PaginatedResponse[AnnouncementResponse])
async def get_announcements(
    session: SessionDep,
    filters: AnnouncementFilter = Depends(),
    user: User | None = Depends(current_user_or_none),
    skip: int = 0,
    limit: int = 10,
) -> PaginatedResponse[AnnouncementResponse]:
    search = AnnouncementSearch(session=session, filters=filters)
    announcements = await search.results(skip=skip, limit=limit)
    filtered_announcements_count = await search.filtered_count()
    total_announcements_count = await search.total_count()
    get_batch_permissions(user, announcements)
    return PaginatedResponse(
        data=announcements,
        skip=skip,
        limit=limit,
        filtered_count=filtered_announcements_count,
        total_count=total_announcements_count,
    )


@router.post("", response_model=DataResponse[AnnouncementResponse], status_code=201)
async def create_announcement(
    session: SessionDep,
    announcement_in: AnnouncementCreate,
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, Announcement, "create")
    scenario = CreateAnnouncementScenario(session)
    announcement = await scenario.run(
        CreateAnnouncementContract(
            announcement_in=announcement_in,
            organizer_id=user.id,
        )
    )
    await session.commit()
    return DataResponse(data=announcement)
