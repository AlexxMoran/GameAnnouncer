from fastapi import APIRouter, Depends

from core.deps import SessionDep
from core.permissions import authorize_action
from core.schemas.base import DataResponse
from core.users import current_user
from domains.announcements.model import Announcement
from domains.announcements.repository import AnnouncementRepository
from domains.matches.model import Match
from domains.matches.repository import MatchRepository
from domains.matches.schemas import MatchResponse, MatchResultUpdate
from domains.matches.services.match_progression import MatchProgressionService
from domains.users.model import User
from exceptions import AppException

router = APIRouter(prefix="/matches", tags=["matches"])


async def get_match_dependency(match_id: int, session: SessionDep) -> Match:
    """Load a match by ID or raise 404."""
    repo = MatchRepository(session)
    match = await repo.find_by_id(match_id)
    if not match:
        raise AppException("Match not found", status_code=404)
    return match


async def get_announcement_for_match_dependency(
    session: SessionDep,
    match: Match = Depends(get_match_dependency),
) -> Announcement:
    """Load the announcement that owns the match, or raise 404."""
    repo = AnnouncementRepository(session)
    announcement = await repo.find_by_id(match.announcement_id)
    if not announcement:
        raise AppException("Announcement not found", status_code=404)
    return announcement


@router.get("/{match_id}", response_model=DataResponse[MatchResponse])
async def get_match(
    match: Match = Depends(get_match_dependency),
) -> DataResponse[MatchResponse]:
    return DataResponse(data=match)


@router.patch("/{match_id}/result", response_model=DataResponse[MatchResponse])
async def set_match_result(
    session: SessionDep,
    result_in: MatchResultUpdate,
    match: Match = Depends(get_match_dependency),
    announcement: Announcement = Depends(get_announcement_for_match_dependency),
    user: User = Depends(current_user),
) -> DataResponse[MatchResponse]:
    """
    Set the winner of a match and advance the bracket.

    Requires organizer or admin privileges on the announcement.
    """
    authorize_action(user, announcement, "manage_lifecycle")
    service = MatchProgressionService(match, announcement, result_in, session)
    match = await service.call()
    await session.commit()
    return DataResponse(data=match)
