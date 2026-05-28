import pytest
from datetime import datetime, timedelta, timezone

from modules.announcements.model import Announcement
from modules.announcements.services.lifecycle import AnnouncementLifecycleService
from modules.announcements.state_machine import AnnouncementStateMachine
from core.utils import as_utc
from modules.games.model import Game
from enums import (
    AnnouncementFormat,
    AnnouncementStatus,
    AnnouncementTrigger,
    SeedMethod,
)
from exceptions import ValidationException


def _make_announcement(
    game_id: int, organizer_id: int, status: AnnouncementStatus
) -> Announcement:
    now = datetime.now(timezone.utc)
    return Announcement(
        title="Test Tournament",
        content="Test",
        game_id=game_id,
        organizer_id=organizer_id,
        status=status,
        registration_start_at=now - timedelta(hours=2),
        registration_end_at=now - timedelta(hours=1),
        start_at=now,
        max_participants=8,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )


async def _setup(db_session, create_user, email: str, status: AnnouncementStatus):
    """Create a persisted user, game, and announcement with the given status."""
    user = await create_user(email=email)
    game = Game(name="Test Game", category="FPS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, status)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    return user, ann


@pytest.mark.asyncio
async def test_open_registration_transitions_to_registration_open(
    db_session, create_user
):
    """open_registration moves PRE_REGISTRATION -> REGISTRATION_OPEN."""
    _, ann = await _setup(
        db_session, create_user, "sm-open@test.com", AnnouncementStatus.PRE_REGISTRATION
    )

    result = await AnnouncementStateMachine(ann, db_session).fire(
        AnnouncementTrigger.OPEN_REGISTRATION
    )

    assert result.status == AnnouncementStatus.REGISTRATION_OPEN


@pytest.mark.asyncio
async def test_close_registration_transitions_to_registration_closed(
    db_session, create_user
):
    """close_registration moves REGISTRATION_OPEN -> REGISTRATION_CLOSED."""
    _, ann = await _setup(
        db_session,
        create_user,
        "sm-close@test.com",
        AnnouncementStatus.REGISTRATION_OPEN,
    )

    result = await AnnouncementStateMachine(ann, db_session).fire(
        AnnouncementTrigger.CLOSE_REGISTRATION
    )

    assert result.status == AnnouncementStatus.REGISTRATION_CLOSED


@pytest.mark.asyncio
async def test_lifecycle_open_registration_sets_actual_start_time(
    db_session, create_user
):
    """Manual registration opening records the actual opening time."""
    _, ann = await _setup(
        db_session,
        create_user,
        "sm-open-time@test.com",
        AnnouncementStatus.PRE_REGISTRATION,
    )
    now = datetime.now(timezone.utc)
    ann.registration_start_at = now + timedelta(hours=1)
    ann.registration_end_at = now + timedelta(hours=2)
    ann.start_at = now + timedelta(hours=3)
    await db_session.commit()

    before = datetime.now(timezone.utc)
    result = await AnnouncementLifecycleService(ann, db_session).open_registration()
    after = datetime.now(timezone.utc)

    assert result.status == AnnouncementStatus.REGISTRATION_OPEN
    assert before <= as_utc(result.registration_start_at) <= after


@pytest.mark.asyncio
async def test_lifecycle_close_registration_sets_actual_end_time(
    db_session, create_user
):
    """Manual registration closing records the actual closing time."""
    _, ann = await _setup(
        db_session,
        create_user,
        "sm-close-time@test.com",
        AnnouncementStatus.REGISTRATION_OPEN,
    )
    now = datetime.now(timezone.utc)
    ann.registration_start_at = now - timedelta(hours=1)
    ann.registration_end_at = now + timedelta(hours=1)
    ann.start_at = now + timedelta(hours=2)
    await db_session.commit()

    before = datetime.now(timezone.utc)
    result = await AnnouncementLifecycleService(ann, db_session).close_registration()
    after = datetime.now(timezone.utc)

    assert result.status == AnnouncementStatus.REGISTRATION_CLOSED
    assert before <= as_utc(result.registration_end_at) <= after


@pytest.mark.asyncio
async def test_lifecycle_open_registration_rejects_invalid_dates(
    db_session, create_user
):
    """Manual registration opening validates the updated registration window."""
    _, ann = await _setup(
        db_session,
        create_user,
        "sm-open-invalid-time@test.com",
        AnnouncementStatus.PRE_REGISTRATION,
    )

    with pytest.raises(ValidationException, match="registration_end_at"):
        await AnnouncementLifecycleService(ann, db_session).open_registration()


@pytest.mark.asyncio
async def test_lifecycle_close_registration_rejects_invalid_dates(
    db_session, create_user
):
    """Manual registration closing validates the updated registration window."""
    _, ann = await _setup(
        db_session,
        create_user,
        "sm-close-invalid-time@test.com",
        AnnouncementStatus.REGISTRATION_OPEN,
    )

    with pytest.raises(ValidationException, match="start_at"):
        await AnnouncementLifecycleService(ann, db_session).close_registration()


@pytest.mark.asyncio
async def test_open_registration_from_wrong_status_raises_validation_exception(
    db_session, create_user
):
    """open_registration from REGISTRATION_OPEN raises ValidationException."""
    _, ann = await _setup(
        db_session,
        create_user,
        "sm-open-wrong@test.com",
        AnnouncementStatus.REGISTRATION_OPEN,
    )

    with pytest.raises(ValidationException, match="open_registration"):
        await AnnouncementStateMachine(ann, db_session).fire(
            AnnouncementTrigger.OPEN_REGISTRATION
        )


@pytest.mark.asyncio
async def test_close_registration_from_wrong_status_raises_validation_exception(
    db_session, create_user
):
    """close_registration from PRE_REGISTRATION raises ValidationException."""
    _, ann = await _setup(
        db_session,
        create_user,
        "sm-close-wrong@test.com",
        AnnouncementStatus.PRE_REGISTRATION,
    )

    with pytest.raises(ValidationException, match="close_registration"):
        await AnnouncementStateMachine(ann, db_session).fire(
            AnnouncementTrigger.CLOSE_REGISTRATION
        )


@pytest.mark.asyncio
async def test_start_qualification_transitions_to_live(db_session, create_user):
    """start_qualification moves REGISTRATION_CLOSED → LIVE."""
    _, ann = await _setup(
        db_session, create_user, "sm1@test.com", AnnouncementStatus.REGISTRATION_CLOSED
    )

    result = await AnnouncementStateMachine(ann, db_session).fire(
        AnnouncementTrigger.START_QUALIFICATION
    )

    assert result.status == AnnouncementStatus.LIVE


@pytest.mark.asyncio
async def test_generate_bracket_from_registration_closed_transitions_to_live(
    db_session, create_user
):
    """generate_bracket moves REGISTRATION_CLOSED → LIVE."""
    _, ann = await _setup(
        db_session, create_user, "sm2@test.com", AnnouncementStatus.REGISTRATION_CLOSED
    )

    result = await AnnouncementStateMachine(ann, db_session).fire(
        AnnouncementTrigger.GENERATE_BRACKET
    )

    assert result.status == AnnouncementStatus.LIVE


@pytest.mark.asyncio
async def test_generate_bracket_from_live_stays_live(db_session, create_user):
    """generate_bracket from LIVE is a self-transition — status stays LIVE."""
    _, ann = await _setup(
        db_session, create_user, "sm3@test.com", AnnouncementStatus.LIVE
    )

    result = await AnnouncementStateMachine(ann, db_session).fire(
        AnnouncementTrigger.GENERATE_BRACKET
    )

    assert result.status == AnnouncementStatus.LIVE


@pytest.mark.asyncio
async def test_finalize_qualification_stays_live(db_session, create_user):
    """finalize_qualification from LIVE is a self-transition — status stays LIVE."""
    _, ann = await _setup(
        db_session, create_user, "sm4@test.com", AnnouncementStatus.LIVE
    )

    result = await AnnouncementStateMachine(ann, db_session).fire(
        AnnouncementTrigger.FINALIZE_QUALIFICATION
    )

    assert result.status == AnnouncementStatus.LIVE


@pytest.mark.asyncio
async def test_cancel_from_live_transitions_to_cancelled(db_session, create_user):
    """cancel moves LIVE → CANCELLED."""
    _, ann = await _setup(
        db_session, create_user, "sm5@test.com", AnnouncementStatus.LIVE
    )

    result = await AnnouncementStateMachine(ann, db_session).fire(
        AnnouncementTrigger.CANCEL
    )

    assert result.status == AnnouncementStatus.CANCELLED


@pytest.mark.asyncio
async def test_cancel_from_pre_registration_transitions_to_cancelled(
    db_session, create_user
):
    """cancel moves PRE_REGISTRATION → CANCELLED."""
    _, ann = await _setup(
        db_session, create_user, "sm6@test.com", AnnouncementStatus.PRE_REGISTRATION
    )

    result = await AnnouncementStateMachine(ann, db_session).fire(
        AnnouncementTrigger.CANCEL
    )

    assert result.status == AnnouncementStatus.CANCELLED


@pytest.mark.asyncio
async def test_auto_finish_transitions_to_finished(db_session, create_user):
    """auto_finish moves LIVE → FINISHED."""
    _, ann = await _setup(
        db_session, create_user, "sm7@test.com", AnnouncementStatus.LIVE
    )

    result = await AnnouncementStateMachine(ann, db_session).fire(
        AnnouncementTrigger.AUTO_FINISH
    )

    assert result.status == AnnouncementStatus.FINISHED


@pytest.mark.asyncio
async def test_invalid_trigger_from_wrong_status_raises_validation_exception(
    db_session, create_user
):
    """Firing start_qualification when LIVE raises ValidationException."""
    _, ann = await _setup(
        db_session, create_user, "sm8@test.com", AnnouncementStatus.LIVE
    )

    with pytest.raises(ValidationException, match="start_qualification"):
        await AnnouncementStateMachine(ann, db_session).fire(
            AnnouncementTrigger.START_QUALIFICATION
        )


@pytest.mark.asyncio
async def test_cancel_from_finished_raises_validation_exception(
    db_session, create_user
):
    """cancel from a terminal state raises ValidationException."""
    _, ann = await _setup(
        db_session, create_user, "sm9@test.com", AnnouncementStatus.FINISHED
    )

    with pytest.raises(ValidationException, match="cancel"):
        await AnnouncementStateMachine(ann, db_session).fire(AnnouncementTrigger.CANCEL)
