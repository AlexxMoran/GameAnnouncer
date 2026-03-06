import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

from domains.announcements.model import Announcement
from domains.announcements.repository import AnnouncementRepository
from domains.games.model import Game
from domains.participants.model import AnnouncementParticipant
from domains.participants.repository import ParticipantRepository
from domains.registration.models import RegistrationRequest
from domains.registration.services.lifecycle import RegistrationLifecycleService
from enums import AnnouncementFormat, SeedMethod
from enums.registration_status import RegistrationStatus
from exceptions import ValidationException


def _make_announcement(
    game_id: int, organizer_id: int, max_participants: int = 10
) -> Announcement:
    now = datetime.now(timezone.utc)
    return Announcement(
        title="Test Announcement",
        content="Test content",
        game_id=game_id,
        organizer_id=organizer_id,
        registration_start_at=now - timedelta(hours=2),
        registration_end_at=now + timedelta(hours=1),
        start_at=now + timedelta(days=1),
        max_participants=max_participants,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )


async def _setup(db_session, create_user, max_participants=10):
    """Create user, game, and announcement for tests."""
    organizer = await create_user(email="organizer@example.com")
    applicant = await create_user(email="applicant@example.com")
    game = Game(name="Test Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, organizer.id, max_participants)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    return organizer, applicant, ann


@pytest.mark.asyncio
async def test_approve_creates_participant(db_session, create_user):
    """Approving a pending request creates an AnnouncementParticipant."""
    _, applicant, ann = await _setup(db_session, create_user)

    rr = RegistrationRequest(
        announcement_id=ann.id,
        user_id=applicant.id,
        status=RegistrationStatus.PENDING,
    )
    db_session.add(rr)
    await db_session.flush()

    lifecycle = RegistrationLifecycleService(rr, ann, db_session)
    result = await lifecycle.approve()

    assert result.status == RegistrationStatus.APPROVED

    repo = ParticipantRepository(db_session)
    participant = await repo.find_by_announcement_and_user(ann.id, applicant.id)
    assert participant is not None


@pytest.mark.asyncio
async def test_reject_pending_does_not_create_participant(db_session, create_user):
    """Rejecting a pending request does not create a participant."""
    _, applicant, ann = await _setup(db_session, create_user)

    rr = RegistrationRequest(
        announcement_id=ann.id,
        user_id=applicant.id,
        status=RegistrationStatus.PENDING,
    )
    db_session.add(rr)
    await db_session.flush()

    lifecycle = RegistrationLifecycleService(rr, ann, db_session)
    result = await lifecycle.reject(reason="Not eligible")

    assert result.status == RegistrationStatus.REJECTED
    assert result.cancellation_reason == "Not eligible"

    repo = ParticipantRepository(db_session)
    participant = await repo.find_by_announcement_and_user(ann.id, applicant.id)
    assert participant is None


@pytest.mark.asyncio
async def test_cancel_approved_removes_participant(db_session, create_user):
    """Cancelling an approved request removes the participant."""
    _, applicant, ann = await _setup(db_session, create_user)

    rr = RegistrationRequest(
        announcement_id=ann.id,
        user_id=applicant.id,
        status=RegistrationStatus.PENDING,
    )
    db_session.add(rr)
    await db_session.flush()

    lifecycle = RegistrationLifecycleService(rr, ann, db_session)
    await lifecycle.approve()

    repo = ParticipantRepository(db_session)
    assert await repo.find_by_announcement_and_user(ann.id, applicant.id) is not None

    lifecycle2 = RegistrationLifecycleService(rr, ann, db_session)
    result = await lifecycle2.cancel()

    assert result.status == RegistrationStatus.CANCELLED
    assert await repo.find_by_announcement_and_user(ann.id, applicant.id) is None


@pytest.mark.asyncio
async def test_approve_fails_when_capacity_reached(db_session, create_user):
    """Approve raises ValidationException when max_participants reached."""
    _, applicant, ann = await _setup(db_session, create_user, max_participants=1)

    existing_user = await create_user(email="existing@example.com")
    participant = AnnouncementParticipant(
        announcement_id=ann.id,
        user_id=existing_user.id,
        is_qualified=False,
    )
    db_session.add(participant)
    await db_session.flush()

    rr = RegistrationRequest(
        announcement_id=ann.id,
        user_id=applicant.id,
        status=RegistrationStatus.PENDING,
    )
    db_session.add(rr)
    await db_session.flush()

    lifecycle = RegistrationLifecycleService(rr, ann, db_session)

    with pytest.raises(ValidationException) as exc_info:
        await lifecycle.approve()

    assert "maximum number of participants" in str(exc_info.value)
    assert rr.status == RegistrationStatus.PENDING


@pytest.mark.asyncio
async def test_illegal_transition_raises(db_session, create_user):
    """Illegal transitions raise ValidationException."""
    _, applicant, ann = await _setup(db_session, create_user)

    rr = RegistrationRequest(
        announcement_id=ann.id,
        user_id=applicant.id,
        status=RegistrationStatus.REJECTED,
    )
    db_session.add(rr)
    await db_session.flush()

    lifecycle = RegistrationLifecycleService(rr, ann, db_session)

    with pytest.raises(ValidationException):
        await lifecycle.approve()


@pytest.mark.asyncio
async def test_approve_invalid_transition_does_not_lock_announcement(
    db_session, create_user, monkeypatch
):
    """Invalid approve transition should fail before announcement locking."""
    _, applicant, ann = await _setup(db_session, create_user)

    rr = RegistrationRequest(
        announcement_id=ann.id,
        user_id=applicant.id,
        status=RegistrationStatus.REJECTED,
    )
    db_session.add(rr)
    await db_session.flush()

    lock_mock = AsyncMock(side_effect=AssertionError("lock should not be called"))
    monkeypatch.setattr(AnnouncementRepository, "find_by_id_for_update", lock_mock)

    lifecycle = RegistrationLifecycleService(rr, ann, db_session)

    with pytest.raises(ValidationException):
        await lifecycle.approve()

    lock_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_approve_raises_when_announcement_not_found(
    db_session, create_user, monkeypatch
):
    """Approve fails cleanly if the locked announcement row is missing."""
    _, applicant, ann = await _setup(db_session, create_user)

    rr = RegistrationRequest(
        announcement_id=ann.id,
        user_id=applicant.id,
        status=RegistrationStatus.PENDING,
    )
    db_session.add(rr)
    await db_session.flush()

    monkeypatch.setattr(
        AnnouncementRepository,
        "find_by_id_for_update",
        AsyncMock(return_value=None),
    )

    lifecycle = RegistrationLifecycleService(rr, ann, db_session)

    with pytest.raises(ValidationException) as exc_info:
        await lifecycle.approve()

    assert "Announcement not found" in str(exc_info.value)
    assert rr.status == RegistrationStatus.PENDING


@pytest.mark.asyncio
async def test_expire_updates_status(db_session, create_user):
    """Expire transitions a pending request and flushes the new status."""
    _, applicant, ann = await _setup(db_session, create_user)

    rr = RegistrationRequest(
        announcement_id=ann.id,
        user_id=applicant.id,
        status=RegistrationStatus.PENDING,
    )
    db_session.add(rr)
    await db_session.flush()

    lifecycle = RegistrationLifecycleService(rr, ann, db_session)
    await lifecycle.expire()

    assert rr.status == RegistrationStatus.EXPIRED


@pytest.mark.asyncio
async def test_system_reject_for_form_change_removes_participant(
    db_session, create_user
):
    """System reject of an approved request removes the participant."""
    _, applicant, ann = await _setup(db_session, create_user)

    rr = RegistrationRequest(
        announcement_id=ann.id,
        user_id=applicant.id,
        status=RegistrationStatus.PENDING,
    )
    db_session.add(rr)
    await db_session.flush()

    lifecycle = RegistrationLifecycleService(rr, ann, db_session)
    await lifecycle.approve()

    repo = ParticipantRepository(db_session)
    assert await repo.find_by_announcement_and_user(ann.id, applicant.id) is not None

    lifecycle2 = RegistrationLifecycleService(rr, ann, db_session)
    await lifecycle2.system_reject_for_form_change()

    assert rr.status == RegistrationStatus.REJECTED
    assert "Registration form has been updated" in rr.cancellation_reason
    assert await repo.find_by_announcement_and_user(ann.id, applicant.id) is None
