import pytest
from datetime import datetime, timedelta, timezone

from domains.announcements.model import Announcement
from domains.games.model import Game
from domains.registration.models import RegistrationRequest
from domains.registration.schemas import RegistrationRequestCreate
from domains.registration.services.create_request import (
    CreateRegistrationRequestService,
)
from exceptions import ValidationException
from enums import AnnouncementFormat, SeedMethod


def _make_announcement(
    game_id: int, organizer_id: int, reg_open: bool = True
) -> Announcement:
    now = datetime.now(timezone.utc)
    reg_start = now - timedelta(hours=1) if reg_open else now + timedelta(hours=1)
    reg_end = reg_start + timedelta(hours=2)
    return Announcement(
        title="Test Announcement",
        content="Test content",
        game_id=game_id,
        organizer_id=organizer_id,
        registration_start_at=reg_start,
        registration_end_at=reg_end,
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )


@pytest.mark.asyncio
async def test_create_registration_request_success(db_session, create_user):
    """Successful creation when registration is open."""
    user = await create_user(email="test@example.com")
    game = Game(name="Test Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, reg_open=True)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=ann,
        user=user,
        registration_request_in=RegistrationRequestCreate(announcement_id=ann.id),
    )
    result = await service.call()

    assert isinstance(result, RegistrationRequest)
    assert result.user_id == user.id


@pytest.mark.asyncio
async def test_create_registration_request_closed_raises(db_session, create_user):
    """Registration raises ValidationException when closed."""
    user = await create_user(email="test2@example.com")
    game = Game(name="Test Game 2", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, reg_open=False)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=ann,
        user=user,
        registration_request_in=RegistrationRequestCreate(announcement_id=ann.id),
    )

    with pytest.raises(ValidationException) as exc_info:
        await service.call()

    assert "Registration is currently closed" in str(exc_info.value)


@pytest.mark.asyncio
async def test_create_registration_request_duplicate_raises(db_session, create_user):
    """Duplicate active request raises ValidationException."""
    user = await create_user(email="test3@example.com")
    game = Game(name="Test Game 3", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, reg_open=True)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr_in = RegistrationRequestCreate(announcement_id=ann.id)

    await CreateRegistrationRequestService(
        session=db_session, announcement=ann, user=user, registration_request_in=rr_in
    ).call()

    with pytest.raises(ValidationException) as exc_info:
        await CreateRegistrationRequestService(
            session=db_session,
            announcement=ann,
            user=user,
            registration_request_in=rr_in,
        ).call()

    assert "already exists" in str(exc_info.value)
