import pytest

from domains.participants.services.update_score import update_participant_score
from exceptions import AppException


@pytest.mark.asyncio
async def test_update_score_sets_qualification_score(
    db_session, create_user, create_announcement, create_participant
):
    """update_participant_score persists the new score on the participant."""
    organizer = await create_user(email="svc_org1@example.com", password="x")
    participant_user = await create_user(email="svc_part1@example.com", password="x")
    announcement = await create_announcement(organizer_id=organizer.id)
    participant = await create_participant(
        announcement_id=announcement.id, user_id=participant_user.id
    )

    updated = await update_participant_score(
        participant_id=participant.id,
        qualification_score=42,
        announcement=announcement,
        session=db_session,
    )
    await db_session.commit()

    assert updated.qualification_score == 42


@pytest.mark.asyncio
async def test_update_score_raises_404_for_missing_participant(
    db_session, create_user, create_announcement
):
    """update_participant_score raises AppException(404) when participant not found."""
    organizer = await create_user(email="svc_org2@example.com", password="x")
    announcement = await create_announcement(organizer_id=organizer.id)

    with pytest.raises(AppException) as exc_info:
        await update_participant_score(
            participant_id=99999,
            qualification_score=10,
            announcement=announcement,
            session=db_session,
        )

    assert exc_info.value.status_code == 404
