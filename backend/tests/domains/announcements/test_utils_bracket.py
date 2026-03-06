import pytest

from domains.announcements.utils.bracket import compute_bracket_size, get_bracket
from domains.matches.schemas import BracketResponse
from enums import AnnouncementStatus
from exceptions import AppException


@pytest.mark.parametrize(
    "n, expected",
    [
        (2, 2),
        (4, 4),
        (8, 8),
        (16, 16),
        (3, 4),
        (5, 4),
        (6, 8),
        (7, 8),
        (9, 8),
        (12, 16),
    ],
)
def test_compute_bracket_size(n: int, expected: int) -> None:
    """Returns the nearest power-of-two bracket size with round-half-up behaviour."""
    assert compute_bracket_size(n) == expected


@pytest.mark.asyncio
async def test_get_bracket_raises_when_no_matches(
    db_session, create_user, create_announcement
):
    """AppException with 404 is raised when no matches exist for the announcement."""
    organizer = await create_user(email="ub_get1@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        status=AnnouncementStatus.LIVE,
    )

    with pytest.raises(AppException) as exc_info:
        await get_bracket(announcement, db_session)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_get_bracket_returns_bracket_response(
    db_session, create_user, create_announcement, create_match
):
    """Returns a BracketResponse instance when matches exist."""
    organizer = await create_user(email="ub_get2@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        bracket_size=2,
        status=AnnouncementStatus.LIVE,
    )
    await create_match(announcement_id=announcement.id, round_number=1, match_number=1)

    result = await get_bracket(announcement, db_session)

    assert isinstance(result, BracketResponse)


@pytest.mark.asyncio
async def test_get_bracket_size_from_announcement(
    db_session, create_user, create_announcement, create_match
):
    """bracket_size in the response matches the announcement's bracket_size."""
    organizer = await create_user(email="ub_get3@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        bracket_size=8,
        status=AnnouncementStatus.LIVE,
    )
    await create_match(announcement_id=announcement.id, round_number=1, match_number=1)

    result = await get_bracket(announcement, db_session)

    assert result.bracket_size == 8


@pytest.mark.asyncio
async def test_get_bracket_rounds_keyed_by_round_number(
    db_session, create_user, create_announcement, create_match
):
    """rounds is a dict keyed by integer round number."""
    organizer = await create_user(email="ub_get4@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        bracket_size=4,
        status=AnnouncementStatus.LIVE,
    )
    await create_match(announcement_id=announcement.id, round_number=1, match_number=1)
    await create_match(announcement_id=announcement.id, round_number=1, match_number=2)
    await create_match(announcement_id=announcement.id, round_number=2, match_number=1)

    result = await get_bracket(announcement, db_session)

    assert set(result.rounds.keys()) == {1, 2}


@pytest.mark.asyncio
async def test_get_bracket_match_count_per_round(
    db_session, create_user, create_announcement, create_match
):
    """Each round contains the correct number of matches."""
    organizer = await create_user(email="ub_get5@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        bracket_size=4,
        status=AnnouncementStatus.LIVE,
    )
    await create_match(announcement_id=announcement.id, round_number=1, match_number=1)
    await create_match(announcement_id=announcement.id, round_number=1, match_number=2)
    await create_match(announcement_id=announcement.id, round_number=2, match_number=1)

    result = await get_bracket(announcement, db_session)

    assert len(result.rounds[1]) == 2
    assert len(result.rounds[2]) == 1
