import math

from sqlalchemy.ext.asyncio import AsyncSession

from modules.announcements.model import Announcement
from modules.matches.queries import MatchQueries
from modules.matches.schemas import BracketResponse, MatchResponse
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


def compute_bracket_slots(size: int) -> list[int]:
    """
    Compute the ordered slot list for standard single-elimination seeding.

    Produces an interleaved list where index pairs (0,1), (2,3)... define R1 matches
    such that seed 1 faces seed N, seed 4 faces seed N-3, etc.
    Example: size=4 → [1, 4, 2, 3] → R1 matches: (1v4, 2v3).

    Raises:
        ValueError: If size is not a power of two >= 2.
    """
    if size < 2 or (size & (size - 1)) != 0:
        raise ValueError(f"bracket_size must be a power of two >= 2, got {size}")
    if size == 2:
        return [1, 2]
    half = compute_bracket_slots(size // 2)
    result = []
    for seed in half:
        result.append(seed)
        result.append(size + 1 - seed)
    return result
