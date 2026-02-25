import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from domains.announcements.model import Announcement
from domains.announcements.schemas import AnnouncementAction
from domains.announcements.services.update_status import update_announcement_status
from domains.games.model import Game
from enums import AnnouncementStatus, AnnouncementFormat, SeedMethod
from exceptions import ValidationException


def _make_announcement(
    game_id: int, organizer_id: int, title: str = "T"
) -> Announcement:
    now = datetime.now(timezone.utc)
    return Announcement(
        title=title,
        content="c",
        game_id=game_id,
        organizer_id=organizer_id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )


@pytest.mark.asyncio
async def test_update_status_finish_success(db_session, create_user):
    """Finishing a LIVE announcement sets status to FINISHED and records end_at."""
    user = await create_user(email="creator6@example.com", password="x")
    game = Game(name="G-finish", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, "ToFinish")
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    ann.status = AnnouncementStatus.LIVE
    await db_session.commit()
    await db_session.refresh(ann)

    with patch("domains.announcements.services.update_status.authorize_action"):
        updated = await update_announcement_status(
            announcement=ann,
            action=AnnouncementAction.FINISH,
            user=user,
            session=db_session,
        )

    assert updated.status == AnnouncementStatus.FINISHED
    assert updated.end_at is not None


@pytest.mark.asyncio
async def test_update_status_finish_wrong_status_raises(db_session, create_user):
    """Finishing a non-LIVE announcement raises ValidationException."""
    user = await create_user(email="creator7@example.com", password="x")
    game = Game(name="G-finish-fail", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, "WrongStatus")
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    with patch("domains.announcements.services.update_status.authorize_action"):
        with pytest.raises(ValidationException) as exc_info:
            await update_announcement_status(
                announcement=ann,
                action=AnnouncementAction.FINISH,
                user=user,
                session=db_session,
            )
    assert "Can only finish announcement when it is 'live'" in str(exc_info.value)


@pytest.mark.asyncio
async def test_update_status_cancel_success(db_session, create_user):
    """Cancelling an announcement sets status to CANCELLED."""
    user = await create_user(email="creator8@example.com", password="x")
    game = Game(name="G-cancel", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, "ToCancel")
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    with patch("domains.announcements.services.update_status.authorize_action"):
        updated = await update_announcement_status(
            announcement=ann,
            action=AnnouncementAction.CANCEL,
            user=user,
            session=db_session,
        )

    assert updated.status == AnnouncementStatus.CANCELLED
