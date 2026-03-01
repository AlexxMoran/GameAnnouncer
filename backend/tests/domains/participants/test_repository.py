import pytest

from domains.participants.repository import ParticipantRepository


@pytest.mark.asyncio
async def test_find_by_id_returns_participant(
    db_session, create_user, create_announcement, create_participant
):
    """find_by_id returns the correct participant when IDs match."""
    organizer = await create_user(email="repo_org1@example.com", password="x")
    participant_user = await create_user(email="repo_part1@example.com", password="x")
    announcement = await create_announcement(organizer_id=organizer.id)
    participant = await create_participant(
        announcement_id=announcement.id, user_id=participant_user.id
    )

    repo = ParticipantRepository(db_session)
    found = await repo.find_by_id_in_announcement(participant.id, announcement.id)

    assert found is not None
    assert found.id == participant.id
    assert found.user_id == participant_user.id


@pytest.mark.asyncio
async def test_find_by_id_returns_none_for_wrong_announcement(
    db_session, create_user, create_announcement, create_participant
):
    """find_by_id returns None when participant belongs to a different announcement."""
    from domains.games.model import Game

    organizer = await create_user(email="repo_org2@example.com", password="x")
    participant_user = await create_user(email="repo_part2@example.com", password="x")

    game = Game(name="G-repo-wrong-ann", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    announcement = await create_announcement(organizer_id=organizer.id, game_id=game.id)
    other_announcement = await create_announcement(
        organizer_id=organizer.id, game_id=game.id
    )
    participant = await create_participant(
        announcement_id=announcement.id, user_id=participant_user.id
    )

    repo = ParticipantRepository(db_session)
    found = await repo.find_by_id_in_announcement(participant.id, other_announcement.id)

    assert found is None


@pytest.mark.asyncio
async def test_find_by_id_returns_none_for_missing_id(
    db_session, create_user, create_announcement
):
    """find_by_id returns None when the participant ID does not exist."""
    organizer = await create_user(email="repo_org3@example.com", password="x")
    announcement = await create_announcement(organizer_id=organizer.id)

    repo = ParticipantRepository(db_session)
    found = await repo.find_by_id_in_announcement(99999, announcement.id)

    assert found is None


@pytest.mark.asyncio
async def test_find_by_id_eagerly_loads_user(
    db_session, create_user, create_announcement, create_participant
):
    """find_by_id loads the related user via selectinload."""
    organizer = await create_user(email="repo_org4@example.com", password="x")
    participant_user = await create_user(email="repo_part4@example.com", password="x")
    announcement = await create_announcement(organizer_id=organizer.id)
    participant = await create_participant(
        announcement_id=announcement.id, user_id=participant_user.id
    )

    repo = ParticipantRepository(db_session)
    found = await repo.find_by_id_in_announcement(participant.id, announcement.id)

    assert found is not None
    assert found.user is not None
    assert found.user.id == participant_user.id


@pytest.mark.asyncio
async def test_find_all_by_announcement_id_sorted_by_created_at_when_no_scores(
    db_session, create_user, create_announcement, create_participant
):
    """Without scores all participants are returned ordered by created_at."""
    organizer = await create_user(email="repo_org5@example.com", password="x")
    u1 = await create_user(email="repo_sort1@example.com", password="x")
    u2 = await create_user(email="repo_sort2@example.com", password="x")
    u3 = await create_user(email="repo_sort3@example.com", password="x")
    announcement = await create_announcement(organizer_id=organizer.id)

    p1 = await create_participant(announcement_id=announcement.id, user_id=u1.id)
    p2 = await create_participant(announcement_id=announcement.id, user_id=u2.id)
    p3 = await create_participant(announcement_id=announcement.id, user_id=u3.id)

    repo = ParticipantRepository(db_session)
    participants, total = await repo.find_all_by_announcement_id(
        announcement.id, limit=10
    )

    assert total == 3
    ids = [p.id for p in participants]
    assert ids == [p1.id, p2.id, p3.id]


@pytest.mark.asyncio
async def test_find_all_by_announcement_id_sorted_by_score_when_scores_exist(
    db_session, create_user, create_announcement, create_participant
):
    """When scores are set participants with scores appear first ordered by score DESC."""
    organizer = await create_user(email="repo_org6@example.com", password="x")
    u1 = await create_user(email="repo_sc1@example.com", password="x")
    u2 = await create_user(email="repo_sc2@example.com", password="x")
    u3 = await create_user(email="repo_sc3@example.com", password="x")
    announcement = await create_announcement(organizer_id=organizer.id)

    p_no_score = await create_participant(
        announcement_id=announcement.id, user_id=u1.id
    )
    p_low = await create_participant(
        announcement_id=announcement.id, user_id=u2.id, qualification_score=10
    )
    p_high = await create_participant(
        announcement_id=announcement.id, user_id=u3.id, qualification_score=99
    )

    repo = ParticipantRepository(db_session)
    participants, total = await repo.find_all_by_announcement_id(
        announcement.id, limit=10
    )

    assert total == 3
    ids = [p.id for p in participants]
    assert ids == [p_high.id, p_low.id, p_no_score.id]
