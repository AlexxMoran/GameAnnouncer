import pytest

from domains.participants.repository import ParticipantRepository


@pytest.mark.asyncio
async def test_find_by_id_returns_participant(
    db_session, create_user, create_announcement, create_participant
):
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
    organizer = await create_user(email="repo_org3@example.com", password="x")
    announcement = await create_announcement(organizer_id=organizer.id)

    repo = ParticipantRepository(db_session)
    found = await repo.find_by_id_in_announcement(99999, announcement.id)

    assert found is None


@pytest.mark.asyncio
async def test_save_persists_participant(db_session, create_user, create_announcement):
    from domains.participants.model import AnnouncementParticipant

    organizer = await create_user(email="repo_org4@example.com", password="x")
    participant_user = await create_user(email="repo_part4@example.com", password="x")
    announcement = await create_announcement(organizer_id=organizer.id)

    participant = AnnouncementParticipant(
        announcement_id=announcement.id,
        user_id=participant_user.id,
    )

    repo = ParticipantRepository(db_session)
    saved = await repo.save(participant)

    assert saved.id is not None
    assert saved.user_id == participant_user.id
