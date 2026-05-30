from fastapi import APIRouter, Depends

from core.deps import SessionDep
from core.permissions import authorize_action
from core.schemas.base import DataResponse
from core.users import current_user
from modules.announcements.model import Announcement
from modules.matches.model import Match
from modules.matches.schemas.mutations import MatchResultUpdate
from modules.matches.schemas.responses import MatchResponse
from modules.users.model import User
from operations.submit_match_result.contract import SubmitMatchResultContract
from operations.submit_match_result.scenario import SubmitMatchResultScenario

from .dependencies import get_announcement_for_match_dependency, get_match_dependency

router = APIRouter()


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
    scenario = SubmitMatchResultScenario(session)
    match = await scenario.run(
        SubmitMatchResultContract(match_id=match.id, winner=result_in.winner)
    )
    await session.commit()
    return DataResponse(data=match)
