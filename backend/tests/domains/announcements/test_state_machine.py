import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from domains.announcements.model import Announcement
from domains.announcements.state_machine import AnnouncementStateMachine
from domains.games.model import Game
from enums import (
    AnnouncementFormat,
    AnnouncementStatus,
    AnnouncementTrigger,
    SeedMethod,
)
from exceptions import AppException, ValidationException


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
async def test_start_qualification_transitions_to_live(db_session, create_user):
    """start_qualification moves REGISTRATION_CLOSED → LIVE."""
    user, ann = await _setup(
        db_session, create_user, "sm1@test.com", AnnouncementStatus.REGISTRATION_CLOSED
    )

    with patch("domains.announcements.state_machine.authorize_action"):
        result = await AnnouncementStateMachine(ann, db_session).fire(
            AnnouncementTrigger.START_QUALIFICATION, user=user
        )

    assert result.status == AnnouncementStatus.LIVE


@pytest.mark.asyncio
async def test_generate_bracket_from_registration_closed_transitions_to_live(
    db_session, create_user
):
    """generate_bracket moves REGISTRATION_CLOSED → LIVE."""
    user, ann = await _setup(
        db_session, create_user, "sm2@test.com", AnnouncementStatus.REGISTRATION_CLOSED
    )

    with patch("domains.announcements.state_machine.authorize_action"):
        result = await AnnouncementStateMachine(ann, db_session).fire(
            AnnouncementTrigger.GENERATE_BRACKET, user=user
        )

    assert result.status == AnnouncementStatus.LIVE


@pytest.mark.asyncio
async def test_generate_bracket_from_live_stays_live(db_session, create_user):
    """generate_bracket from LIVE is a self-transition — status stays LIVE."""
    user, ann = await _setup(
        db_session, create_user, "sm3@test.com", AnnouncementStatus.LIVE
    )

    with patch("domains.announcements.state_machine.authorize_action"):
        result = await AnnouncementStateMachine(ann, db_session).fire(
            AnnouncementTrigger.GENERATE_BRACKET, user=user
        )

    assert result.status == AnnouncementStatus.LIVE


@pytest.mark.asyncio
async def test_finalize_qualification_stays_live(db_session, create_user):
    """finalize_qualification from LIVE is a self-transition — status stays LIVE."""
    user, ann = await _setup(
        db_session, create_user, "sm4@test.com", AnnouncementStatus.LIVE
    )

    with patch("domains.announcements.state_machine.authorize_action"):
        result = await AnnouncementStateMachine(ann, db_session).fire(
            AnnouncementTrigger.FINALIZE_QUALIFICATION, user=user
        )

    assert result.status == AnnouncementStatus.LIVE


@pytest.mark.asyncio
async def test_cancel_from_live_transitions_to_cancelled(db_session, create_user):
    """cancel moves LIVE → CANCELLED."""
    user, ann = await _setup(
        db_session, create_user, "sm5@test.com", AnnouncementStatus.LIVE
    )

    with patch("domains.announcements.state_machine.authorize_action"):
        result = await AnnouncementStateMachine(ann, db_session).fire(
            AnnouncementTrigger.CANCEL, user=user
        )

    assert result.status == AnnouncementStatus.CANCELLED


@pytest.mark.asyncio
async def test_cancel_from_pre_registration_transitions_to_cancelled(
    db_session, create_user
):
    """cancel moves PRE_REGISTRATION → CANCELLED."""
    user, ann = await _setup(
        db_session, create_user, "sm6@test.com", AnnouncementStatus.PRE_REGISTRATION
    )

    with patch("domains.announcements.state_machine.authorize_action"):
        result = await AnnouncementStateMachine(ann, db_session).fire(
            AnnouncementTrigger.CANCEL, user=user
        )

    assert result.status == AnnouncementStatus.CANCELLED


@pytest.mark.asyncio
async def test_auto_finish_transitions_to_finished_without_user(
    db_session, create_user
):
    """auto_finish moves LIVE → FINISHED with no user — no auth check."""
    user, ann = await _setup(
        db_session, create_user, "sm7@test.com", AnnouncementStatus.LIVE
    )

    result = await AnnouncementStateMachine(ann, db_session).fire(
        AnnouncementTrigger.AUTO_FINISH, user=None
    )

    assert result.status == AnnouncementStatus.FINISHED


@pytest.mark.asyncio
async def test_invalid_trigger_from_wrong_status_raises_validation_exception(
    db_session, create_user
):
    """Firing start_qualification when LIVE raises ValidationException."""
    user, ann = await _setup(
        db_session, create_user, "sm8@test.com", AnnouncementStatus.LIVE
    )

    with pytest.raises(ValidationException, match="start_qualification"):
        with patch("domains.announcements.state_machine.authorize_action"):
            await AnnouncementStateMachine(ann, db_session).fire(
                AnnouncementTrigger.START_QUALIFICATION, user=user
            )


@pytest.mark.asyncio
async def test_cancel_from_finished_raises_validation_exception(
    db_session, create_user
):
    """cancel from a terminal state raises ValidationException."""
    user, ann = await _setup(
        db_session, create_user, "sm9@test.com", AnnouncementStatus.FINISHED
    )

    with pytest.raises(ValidationException, match="cancel"):
        with patch("domains.announcements.state_machine.authorize_action"):
            await AnnouncementStateMachine(ann, db_session).fire(
                AnnouncementTrigger.CANCEL, user=user
            )


@pytest.mark.asyncio
async def test_unauthorized_user_cannot_fire_transition(db_session, create_user):
    """_auth blocks a user without manage_lifecycle permission."""
    user, ann = await _setup(
        db_session, create_user, "sm10@test.com", AnnouncementStatus.LIVE
    )

    with patch(
        "domains.announcements.state_machine.authorize_action",
        side_effect=AppException("Forbidden", status_code=403),
    ):
        with pytest.raises(AppException) as exc_info:
            await AnnouncementStateMachine(ann, db_session).fire(
                AnnouncementTrigger.CANCEL, user=user
            )

    assert exc_info.value.status_code == 403
