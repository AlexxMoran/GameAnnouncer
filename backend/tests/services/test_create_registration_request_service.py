import pytest
from datetime import datetime, timedelta
from services.create_registration_request_service import (
    CreateRegistrationRequestService,
)
from schemas.registration_request import RegistrationRequestCreate
from models.announcement import Announcement
from models.game import Game
from models.registration_request import RegistrationRequest
from exceptions import ValidationException


@pytest.mark.asyncio
async def test_create_registration_request_success(db_session, create_user):
    """Test successful creation of registration request when registration is open."""
    user = await create_user(email="test@example.com")
    game = Game(name="Test Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Test Announcement",
        content="Test content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now - timedelta(hours=1),  # started 1 hour ago
        registration_end_at=now + timedelta(hours=1),  # ends in 1 hour
        start_at=now + timedelta(days=1),
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    registration_request_in = RegistrationRequestCreate(announcement_id=announcement.id)

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=announcement,
        user=user,
        registration_request_in=registration_request_in,
    )

    result = await service.call()

    assert isinstance(result, RegistrationRequest)
    assert result.user_id == user.id
    assert result.announcement_id == announcement.id


@pytest.mark.asyncio
async def test_create_registration_request_before_start(db_session, create_user):
    """Test that registration fails when registration hasn't started yet."""
    user = await create_user(email="early@example.com")
    game = Game(name="Future Game", category="MOBA", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Future Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now + timedelta(hours=1),  # starts in 1 hour
        registration_end_at=now + timedelta(hours=2),
        start_at=now + timedelta(days=1),
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    registration_request_in = RegistrationRequestCreate(announcement_id=announcement.id)

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=announcement,
        user=user,
        registration_request_in=registration_request_in,
    )

    with pytest.raises(ValidationException) as exc_info:
        await service.call()

    assert "Registration is currently closed" in str(exc_info.value)
    assert exc_info.value.status_code == 422


@pytest.mark.asyncio
async def test_create_registration_request_after_end(db_session, create_user):
    """Test that registration fails when registration has already ended."""
    user = await create_user(email="late@example.com")
    game = Game(name="Past Game", category="FPS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Past Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now - timedelta(hours=2),  # started 2 hours ago
        registration_end_at=now - timedelta(hours=1),  # ended 1 hour ago
        start_at=now + timedelta(days=1),
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    registration_request_in = RegistrationRequestCreate(announcement_id=announcement.id)

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=announcement,
        user=user,
        registration_request_in=registration_request_in,
    )

    with pytest.raises(ValidationException) as exc_info:
        await service.call()

    assert "Registration is currently closed" in str(exc_info.value)
    assert exc_info.value.status_code == 422


@pytest.mark.asyncio
async def test_create_registration_request_at_exact_start(db_session, create_user):
    """Test registration at exact start time."""
    user = await create_user(email="exact@example.com")
    game = Game(name="Exact Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Exact Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now,  # starts now
        registration_end_at=now + timedelta(hours=1),
        start_at=now + timedelta(days=1),
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    registration_request_in = RegistrationRequestCreate(announcement_id=announcement.id)

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=announcement,
        user=user,
        registration_request_in=registration_request_in,
    )

    result = await service.call()

    assert result.user_id == user.id
    assert result.announcement_id == announcement.id
