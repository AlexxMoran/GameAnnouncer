from fastapi import APIRouter, Depends, Query

from core.deps import SessionDep
from core.schemas.base import DataResponse, PaginatedResponse
from modules.announcements.model import Announcement
from modules.announcements.utils.bracket import get_bracket
from modules.matches.queries import MatchQueries
from modules.matches.schemas.responses import BracketResponse, MatchResponse

from .dependencies import get_announcement_dependency

router = APIRouter()


@router.get(
    "/{announcement_id}/matches",
    response_model=PaginatedResponse[MatchResponse],
)
async def get_announcement_matches(
    session: SessionDep,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    announcement: Announcement = Depends(get_announcement_dependency),
) -> PaginatedResponse[MatchResponse]:
    queries = MatchQueries(session)
    matches, total = await queries.find_all_by_announcement_id(
        announcement_id=announcement.id, skip=skip, limit=limit
    )
    return PaginatedResponse(
        data=matches, skip=skip, limit=limit, filtered_count=total, total_count=total
    )


@router.get(
    "/{announcement_id}/bracket",
    response_model=DataResponse[BracketResponse],
)
async def get_announcement_bracket(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
) -> DataResponse[BracketResponse]:
    data = await get_bracket(announcement, session)

    return DataResponse(data=data)
