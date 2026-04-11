import pytest

from domains.matches.model import Match
from domains.matches.repository import MatchRepository
from enums import MatchStatus


@pytest.mark.asyncio
async def test_find_by_id_returns_match(
    db_session, create_user, create_announcement, create_match
):
    organizer = await create_user(email="mr_org1@example.com")
    announcement = await create_announcement(organizer_id=organizer.id)
    match = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
    )

    repo = MatchRepository(db_session)
    found = await repo.find_by_id(match.id)

    assert found is not None
    assert found.id == match.id


@pytest.mark.asyncio
async def test_save_many_persists_matches(db_session, create_user, create_announcement):
    organizer = await create_user(email="mr_org2@example.com")
    announcement = await create_announcement(organizer_id=organizer.id)

    matches = [
        Match(announcement_id=announcement.id, round_number=1, match_number=1),
        Match(announcement_id=announcement.id, round_number=1, match_number=2),
    ]

    repo = MatchRepository(db_session)
    saved = await repo.save_many(matches)

    assert len(saved) == 2
    assert all(match.id is not None for match in saved)


@pytest.mark.asyncio
async def test_exists_for_announcement_returns_true_when_matches_exist(
    db_session, create_user, create_announcement, create_match
):
    organizer = await create_user(email="mr_org3@example.com")
    announcement = await create_announcement(organizer_id=organizer.id)
    await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
    )

    repo = MatchRepository(db_session)

    assert await repo.exists_for_announcement(announcement.id) is True


@pytest.mark.asyncio
async def test_has_unfinished_non_bye_matches_ignores_completed_and_byes(
    db_session, create_user, create_announcement, create_match
):
    organizer = await create_user(email="mr_org4@example.com")
    announcement = await create_announcement(organizer_id=organizer.id)
    await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        status=MatchStatus.COMPLETED,
    )
    await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=2,
        is_bye=True,
        status=MatchStatus.PENDING,
    )

    repo = MatchRepository(db_session)

    assert await repo.has_unfinished_non_bye_matches(announcement.id) is False


@pytest.mark.asyncio
async def test_find_third_place_match_returns_only_third_place(
    db_session, create_user, create_announcement, create_match
):
    organizer = await create_user(email="mr_org5@example.com")
    announcement = await create_announcement(organizer_id=organizer.id)
    await create_match(
        announcement_id=announcement.id,
        round_number=2,
        match_number=1,
        is_third_place=False,
    )
    third_place = await create_match(
        announcement_id=announcement.id,
        round_number=2,
        match_number=2,
        is_third_place=True,
    )

    repo = MatchRepository(db_session)
    found = await repo.find_third_place_match(announcement.id)

    assert found is not None
    assert found.id == third_place.id
