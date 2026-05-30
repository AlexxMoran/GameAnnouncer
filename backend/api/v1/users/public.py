from fastapi import APIRouter

from core.deps import SessionDep
from core.schemas.base import PaginatedResponse
from modules.announcements.queries import AnnouncementQueries
from modules.announcements.schemas.responses import AnnouncementResponse

router = APIRouter()


@router.get(
    "/{user_id}/organized_announcements",
    response_model=PaginatedResponse[AnnouncementResponse],
)
async def get_user_organized_announcements(
    user_id: int,
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
) -> PaginatedResponse[AnnouncementResponse]:
    queries = AnnouncementQueries(session)
    announcements, total = await queries.find_all_by_organizer_id(
        user_id, skip=skip, limit=limit
    )
    return PaginatedResponse(
        data=announcements,
        skip=skip,
        limit=limit,
        filtered_count=total,
        total_count=total,
    )
