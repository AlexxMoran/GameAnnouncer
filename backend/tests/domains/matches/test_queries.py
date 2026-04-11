import pytest

from domains.matches.queries import MatchQueries


@pytest.mark.asyncio
async def test_find_by_id_returns_match_with_participants(
    db_session, create_user, create_announcement, create_participant, create_match
):
    organizer = await create_user(email="mq_org1@example.com")
    announcement = await create_announcement(organizer_id=organizer.id)
    user1 = await create_user(email="mq_u1@example.com")
    user2 = await create_user(email="mq_u2@example.com")
    participant1 = await create_participant(
        announcement_id=announcement.id, user_id=user1.id
    )
    participant2 = await create_participant(
        announcement_id=announcement.id, user_id=user2.id
    )
    match = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        participant1_id=participant1.id,
        participant2_id=participant2.id,
    )

    queries = MatchQueries(db_session)
    found = await queries.find_by_id(match.id)

    assert found is not None
    assert found.id == match.id
    assert found.participant1 is not None
    assert found.participant2 is not None


@pytest.mark.asyncio
async def test_find_all_by_announcement_id_returns_ordered_matches(
    db_session, create_user, create_announcement, create_match
):
    organizer = await create_user(email="mq_org2@example.com")
    announcement = await create_announcement(organizer_id=organizer.id)

    match2 = await create_match(
        announcement_id=announcement.id,
        round_number=2,
        match_number=1,
    )
    match1 = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=2,
    )
    match0 = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
    )

    queries = MatchQueries(db_session)
    matches, total = await queries.find_all_by_announcement_id(announcement.id)

    assert total == 3
    assert [match.id for match in matches] == [match0.id, match1.id, match2.id]
