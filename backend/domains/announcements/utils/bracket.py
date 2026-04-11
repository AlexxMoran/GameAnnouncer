import math

from sqlalchemy.ext.asyncio import AsyncSession

from domains.announcements.model import Announcement
from domains.matches.queries import MatchQueries
from domains.matches.schemas import BracketResponse, MatchResponse
from exceptions import AppException


async def get_bracket(
    announcement: Announcement, session: AsyncSession
) -> BracketResponse:
    """
    Fetch all matches for the announcement and group them by round number.

    Raises:
        AppException: If no matches exist (bracket not yet generated).
    """
    matches = await MatchQueries(session).find_all_unpaginated_by_announcement_id(
        announcement.id
    )
    if not matches:
        raise AppException("Bracket has not been generated yet", status_code=404)

    rounds: dict[int, list[MatchResponse]] = {}
    for match in matches:
        rounds.setdefault(match.round_number, []).append(
            MatchResponse.model_validate(match)
        )

    return BracketResponse(bracket_size=announcement.bracket_size, rounds=rounds)


def compute_bracket_size(n: int) -> int:
    """
    Compute the nearest power-of-two bracket size for n participants.

    If n is exactly a power of two, returns n (no BYEs, no cuts).
    If n is closer to the lower power → lower bracket (bottom participants cut).
    If n is closer to the upper power or equidistant → upper bracket (BYEs for top seeds).
    """
    lower = 2 ** math.floor(math.log2(n))
    if lower == n:
        return n
    upper = lower * 2
    if n - lower < upper - n:
        return lower
    return upper
