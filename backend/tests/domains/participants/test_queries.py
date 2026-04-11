import pytest

from domains.participants.queries import ParticipantQueries


@pytest.mark.asyncio
async def test_find_all_by_announcement_id_sorted_by_created_at_when_no_scores(
    db_session, create_user, create_announcement, create_participant
):
    organizer = await create_user(email="repo_org5@example.com", password="x")
    u1 = await create_user(email="repo_sort1@example.com", password="x")
    u2 = await create_user(email="repo_sort2@example.com", password="x")
    u3 = await create_user(email="repo_sort3@example.com", password="x")
    announcement = await create_announcement(organizer_id=organizer.id)

    p1 = await create_participant(announcement_id=announcement.id, user_id=u1.id)
    p2 = await create_participant(announcement_id=announcement.id, user_id=u2.id)
    p3 = await create_participant(announcement_id=announcement.id, user_id=u3.id)

    queries = ParticipantQueries(db_session)
    participants, total = await queries.find_all_by_announcement_id(
        announcement.id, limit=10
    )

    assert total == 3
    ids = [participant.id for participant in participants]
    assert ids == [p1.id, p2.id, p3.id]


@pytest.mark.asyncio
async def test_find_all_by_announcement_id_sorted_by_score_when_scores_exist(
    db_session, create_user, create_announcement, create_participant
):
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

    queries = ParticipantQueries(db_session)
    participants, total = await queries.find_all_by_announcement_id(
        announcement.id, limit=10
    )

    assert total == 3
    ids = [participant.id for participant in participants]
    assert ids == [p_high.id, p_low.id, p_no_score.id]
