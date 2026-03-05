import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domains.announcements.model import Announcement
from domains.announcements.services.finalize_qualification import (
    FinalizeQualificationService,
)
from enums import AnnouncementStatus
from exceptions import ValidationException


async def _reload(db_session, announcement_id: int) -> Announcement:
    """Reload announcement with participants eagerly loaded.

    Uses populate_existing=True to bypass the session identity map and
    ensure freshly created participants are reflected on the returned object.
    """
    result = await db_session.execute(
        select(Announcement)
        .options(selectinload(Announcement.participants))
        .where(Announcement.id == announcement_id)
        .execution_options(populate_existing=True)
    )
    return result.scalar_one()


@pytest.mark.asyncio
async def test_finalize_assigns_ranks_by_score_descending(
    db_session, create_user, create_announcement, create_participant
):
    """Participants are ranked 1, 2, 3 … by qualification score descending."""
    organizer = await create_user(email="fq_org1@example.com")
    u1 = await create_user(email="fq_u1@example.com")
    u2 = await create_user(email="fq_u2@example.com")
    u3 = await create_user(email="fq_u3@example.com")

    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=True,
        status=AnnouncementStatus.LIVE,
    )
    p_low = await create_participant(
        announcement_id=announcement.id, user_id=u1.id, qualification_score=50
    )
    p_high = await create_participant(
        announcement_id=announcement.id, user_id=u2.id, qualification_score=90
    )
    p_mid = await create_participant(
        announcement_id=announcement.id, user_id=u3.id, qualification_score=70
    )

    announcement = await _reload(db_session, announcement.id)

    await FinalizeQualificationService(announcement, db_session, organizer).call()
    await db_session.commit()

    await db_session.refresh(p_high)
    await db_session.refresh(p_mid)
    await db_session.refresh(p_low)

    assert p_high.qualification_rank == 1
    assert p_mid.qualification_rank == 2
    assert p_low.qualification_rank == 3


@pytest.mark.asyncio
async def test_finalize_equal_scores_ordered_by_registration_time(
    db_session, create_user, create_announcement, create_participant
):
    """Participants with equal scores are ranked by created_at ascending."""
    organizer = await create_user(email="fq_org2@example.com")
    u1 = await create_user(email="fq_u2a@example.com")
    u2 = await create_user(email="fq_u2b@example.com")

    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=True,
        status=AnnouncementStatus.LIVE,
    )
    p_first = await create_participant(
        announcement_id=announcement.id, user_id=u1.id, qualification_score=80
    )
    p_second = await create_participant(
        announcement_id=announcement.id, user_id=u2.id, qualification_score=80
    )

    announcement = await _reload(db_session, announcement.id)

    await FinalizeQualificationService(announcement, db_session, organizer).call()
    await db_session.commit()

    await db_session.refresh(p_first)
    await db_session.refresh(p_second)

    assert p_first.qualification_rank == 1
    assert p_second.qualification_rank == 2


@pytest.mark.asyncio
async def test_finalize_sets_is_qualified_for_top_bracket_size(
    db_session, create_user, create_announcement, create_participant
):
    """Only top bracket_size participants are marked as qualified.

    5 participants → bracket_size = 4 (lower, since 5-4=1 < 8-5=3).
    Rank 1–4 get is_qualified=True, rank 5 gets is_qualified=False.
    """
    organizer = await create_user(email="fq_org3@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=True,
        status=AnnouncementStatus.LIVE,
    )

    participants = []
    for i, score in enumerate([90, 80, 70, 60, 50], start=1):
        u = await create_user(email=f"fq_u3_{i}@example.com")
        p = await create_participant(
            announcement_id=announcement.id, user_id=u.id, qualification_score=score
        )
        participants.append(p)

    announcement = await _reload(db_session, announcement.id)

    await FinalizeQualificationService(announcement, db_session, organizer).call()
    await db_session.commit()

    for p in participants:
        await db_session.refresh(p)

    qualified = [p for p in participants if p.is_qualified]
    not_qualified = [p for p in participants if not p.is_qualified]

    assert len(qualified) == 4
    assert len(not_qualified) == 1
    assert not_qualified[0].qualification_score == 50


@pytest.mark.asyncio
async def test_finalize_unscored_participant_is_not_qualified(
    db_session, create_user, create_announcement, create_participant
):
    """Unscored participant is ranked last and never marked as qualified,
    even when bracket_size would numerically include their rank position."""
    organizer = await create_user(email="fq_org4@example.com")
    u1 = await create_user(email="fq_u4a@example.com")
    u2 = await create_user(email="fq_u4b@example.com")

    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=True,
        status=AnnouncementStatus.LIVE,
    )
    p_scored = await create_participant(
        announcement_id=announcement.id, user_id=u1.id, qualification_score=80
    )
    p_unscored = await create_participant(
        announcement_id=announcement.id, user_id=u2.id
    )

    announcement = await _reload(db_session, announcement.id)

    await FinalizeQualificationService(announcement, db_session, organizer).call()
    await db_session.commit()

    await db_session.refresh(p_scored)
    await db_session.refresh(p_unscored)

    assert p_scored.qualification_rank == 1
    assert p_unscored.qualification_rank == 2
    assert p_scored.is_qualified is True
    assert p_unscored.is_qualified is False


@pytest.mark.asyncio
async def test_finalize_sets_bracket_size_on_announcement(
    db_session, create_user, create_announcement, create_participant
):
    """announcement.bracket_size is computed and persisted."""
    organizer = await create_user(email="fq_org5@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=True,
        status=AnnouncementStatus.LIVE,
    )

    for i in range(1, 4):
        u = await create_user(email=f"fq_u5_{i}@example.com")
        await create_participant(
            announcement_id=announcement.id, user_id=u.id, qualification_score=i * 10
        )

    announcement = await _reload(db_session, announcement.id)

    result = await FinalizeQualificationService(
        announcement, db_session, organizer
    ).call()
    await db_session.commit()

    assert result.bracket_size == 4


@pytest.mark.asyncio
async def test_finalize_sets_qualification_finished_flag(
    db_session, create_user, create_announcement, create_participant
):
    """announcement.qualification_finished is True after finalization."""
    organizer = await create_user(email="fq_org6@example.com")
    u = await create_user(email="fq_u6@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=True,
        status=AnnouncementStatus.LIVE,
    )
    await create_participant(
        announcement_id=announcement.id, user_id=u.id, qualification_score=50
    )

    announcement = await _reload(db_session, announcement.id)

    result = await FinalizeQualificationService(
        announcement, db_session, organizer
    ).call()
    await db_session.commit()

    assert result.qualification_finished is True


@pytest.mark.asyncio
async def test_finalize_raises_when_no_qualification_phase(
    db_session, create_user, create_announcement
):
    """ValidationException when has_qualification is False."""
    organizer = await create_user(email="fq_org7@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=False,
        status=AnnouncementStatus.LIVE,
    )

    with pytest.raises(
        ValidationException, match="does not have a qualification phase"
    ):
        await FinalizeQualificationService(announcement, db_session, organizer).call()


@pytest.mark.asyncio
async def test_finalize_raises_when_already_finished(
    db_session, create_user, create_announcement
):
    """ValidationException when qualification_finished is already True."""
    organizer = await create_user(email="fq_org8@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=True,
        qualification_finished=True,
        status=AnnouncementStatus.LIVE,
    )

    with pytest.raises(ValidationException, match="already been finalized"):
        await FinalizeQualificationService(announcement, db_session, organizer).call()


@pytest.mark.asyncio
async def test_finalize_raises_when_no_participants(
    db_session, create_user, create_announcement
):
    """ValidationException when announcement has no participants."""
    organizer = await create_user(email="fq_org9@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=True,
        status=AnnouncementStatus.LIVE,
    )
    announcement = await _reload(db_session, announcement.id)

    with pytest.raises(ValidationException, match="No participants"):
        await FinalizeQualificationService(announcement, db_session, organizer).call()


@pytest.mark.asyncio
async def test_finalize_raises_when_status_is_not_live(
    db_session, create_user, create_announcement
):
    """ValidationException when announcement is not in LIVE status."""
    organizer = await create_user(email="fq_org10@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=True,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )

    with pytest.raises(ValidationException, match="not allowed"):
        await FinalizeQualificationService(announcement, db_session, organizer).call()
