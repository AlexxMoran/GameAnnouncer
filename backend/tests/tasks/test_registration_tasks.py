import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy import select, and_
from tasks.registration_request_tasks import expire_registration_requests_task
from models.announcement import Announcement
from models.game import Game
from models.registration_request import RegistrationRequest
from enums.registration_status import RegistrationStatus


@pytest.mark.asyncio
async def test_expire_registration_requests_no_expired(db_session, create_user):
    """Test task when there are no expired requests."""
    user = await create_user(email="active@example.com")
    game = Game(name="Active Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Active Announcement",
        content="c",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now - timedelta(hours=1),
        registration_end_at=now + timedelta(hours=1),
        start_at=now + timedelta(days=1),
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    registration_request = RegistrationRequest(
        announcement_id=announcement.id,
        user_id=user.id,
        status=RegistrationStatus.PENDING,
    )
    db_session.add(registration_request)
    await db_session.commit()

    result = await expire_registration_requests_task()

    assert result == 0
    await db_session.refresh(registration_request)
    assert registration_request.status == RegistrationStatus.PENDING


@pytest.mark.asyncio
async def test_expire_registration_requests_with_expired(db_session, create_user):
    """Test task expires PENDING requests with past registration_end_at."""
    user = await create_user(email="expired@example.com")
    game = Game(name="Expired Game", category="MOBA", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Expired Announcement",
        content="c",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now - timedelta(hours=2),
        registration_end_at=now - timedelta(hours=1),
        start_at=now + timedelta(days=1),
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    registration_request = RegistrationRequest(
        announcement_id=announcement.id,
        user_id=user.id,
        status=RegistrationStatus.PENDING,
    )
    db_session.add(registration_request)
    await db_session.commit()
    await db_session.refresh(registration_request)

    # Mock create_db to return our test session
    mock_db = MagicMock()
    mock_db.session_factory.return_value.__aenter__.return_value = db_session
    mock_db.session_factory.return_value.__aexit__.return_value = AsyncMock()

    import tasks.registration_request_tasks
    original_create_db = tasks.registration_request_tasks.create_db
    tasks.registration_request_tasks.create_db = lambda: mock_db

    try:
        result = await expire_registration_requests_task()

        assert result == 1
        await db_session.refresh(registration_request)
        assert registration_request.status == RegistrationStatus.EXPIRED
    finally:
        tasks.registration_request_tasks.create_db = original_create_db


@pytest.mark.asyncio
async def test_expire_registration_requests_multiple_expired(db_session, create_user):
    """Test task expires multiple PENDING requests."""
    user1 = await create_user(email="user1@example.com")
    user2 = await create_user(email="user2@example.com")
    game = Game(name="Multi Game", category="FPS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Multi Announcement",
        content="c",
        game_id=game.id,
        organizer_id=user1.id,
        registration_start_at=now - timedelta(hours=3),
        registration_end_at=now - timedelta(hours=1),  # ended
        start_at=now + timedelta(days=1),
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    request1 = RegistrationRequest(
        announcement_id=announcement.id,
        user_id=user1.id,
        status=RegistrationStatus.PENDING,
    )
    request2 = RegistrationRequest(
        announcement_id=announcement.id,
        user_id=user2.id,
        status=RegistrationStatus.PENDING,
    )
    db_session.add(request1)
    db_session.add(request2)
    await db_session.commit()
    await db_session.refresh(request1)
    await db_session.refresh(request2)

    mock_db = MagicMock()
    mock_db.session_factory.return_value.__aenter__.return_value = db_session
    mock_db.session_factory.return_value.__aexit__.return_value = AsyncMock()

    import tasks.registration_request_tasks
    original_create_db = tasks.registration_request_tasks.create_db
    tasks.registration_request_tasks.create_db = lambda: mock_db

    try:
        result = await expire_registration_requests_task()

        assert result == 2
        await db_session.refresh(request1)
        await db_session.refresh(request2)
        assert request1.status == RegistrationStatus.EXPIRED
        assert request2.status == RegistrationStatus.EXPIRED
    finally:
        tasks.registration_request_tasks.create_db = original_create_db


@pytest.mark.asyncio
async def test_expire_registration_requests_ignores_approved(db_session, create_user):
    """Test task doesn't expire APPROVED requests."""
    user = await create_user(email="approved@example.com")
    game = Game(name="Approved Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Approved Announcement",
        content="c",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now - timedelta(hours=2),
        registration_end_at=now - timedelta(hours=1),
        start_at=now + timedelta(days=1),
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    approved_request = RegistrationRequest(
        announcement_id=announcement.id,
        user_id=user.id,
        status=RegistrationStatus.APPROVED,
    )
    db_session.add(approved_request)
    await db_session.commit()

    result = await expire_registration_requests_task()

    assert result == 0
    await db_session.refresh(approved_request)
    assert approved_request.status == RegistrationStatus.APPROVED


@pytest.mark.asyncio
async def test_expire_registration_requests_mixed_statuses(db_session, create_user):
    """Test task only expires PENDING requests with past deadline."""
    user1 = await create_user(email="mixed1@example.com")
    user2 = await create_user(email="mixed2@example.com")
    user3 = await create_user(email="mixed3@example.com")
    game = Game(name="Mixed Game", category="RPG", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Mixed Announcement",
        content="c",
        game_id=game.id,
        organizer_id=user1.id,
        registration_start_at=now - timedelta(hours=2),
        registration_end_at=now - timedelta(hours=1),
        start_at=now + timedelta(days=1),
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    pending_request = RegistrationRequest(
        announcement_id=announcement.id,
        user_id=user1.id,
        status=RegistrationStatus.PENDING,
    )
    approved_request = RegistrationRequest(
        announcement_id=announcement.id,
        user_id=user2.id,
        status=RegistrationStatus.APPROVED,
    )
    rejected_request = RegistrationRequest(
        announcement_id=announcement.id,
        user_id=user3.id,
        status=RegistrationStatus.REJECTED,
    )
    db_session.add(pending_request)
    db_session.add(approved_request)
    db_session.add(rejected_request)
    await db_session.commit()
    await db_session.refresh(pending_request)
    await db_session.refresh(approved_request)
    await db_session.refresh(rejected_request)

    mock_db = MagicMock()
    mock_db.session_factory.return_value.__aenter__.return_value = db_session
    mock_db.session_factory.return_value.__aexit__.return_value = AsyncMock()

    import tasks.registration_request_tasks
    original_create_db = tasks.registration_request_tasks.create_db
    tasks.registration_request_tasks.create_db = lambda: mock_db

    try:
        result = await expire_registration_requests_task()

        assert result == 1
        await db_session.refresh(pending_request)
        await db_session.refresh(approved_request)
        await db_session.refresh(rejected_request)
        assert pending_request.status == RegistrationStatus.EXPIRED
        assert approved_request.status == RegistrationStatus.APPROVED
        assert rejected_request.status == RegistrationStatus.REJECTED
    finally:
        tasks.registration_request_tasks.create_db = original_create_db
