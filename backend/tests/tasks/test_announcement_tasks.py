import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, AsyncMock
from tasks.announcement_tasks import update_announcement_statuses
from models.announcement import Announcement
from models.game import Game
from enums import AnnouncementStatus, AnnouncementFormat, SeedMethod


@pytest.mark.asyncio
async def test_update_announcement_statuses_no_changes(db_session, create_user):
    """Test task when no announcements need status updates."""
    user = await create_user(email="organizer@example.com")
    game = Game(name="Test Game", category="RTS", description="Test game")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    announcement = Announcement(
        title="Future Announcement",
        content="Test content",
        game_id=game.id,
        organizer_id=user.id,
        status=AnnouncementStatus.PRE_REGISTRATION,
        registration_start_at=now + timedelta(hours=1),
        registration_end_at=now + timedelta(hours=2),
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.commit()

    mock_db = MagicMock()
    mock_db.session_factory.return_value.__aenter__.return_value = db_session
    mock_db.session_factory.return_value.__aexit__.return_value = AsyncMock()

    import tasks.announcement_tasks

    original_create_db = tasks.announcement_tasks.create_db
    tasks.announcement_tasks.create_db = lambda: mock_db

    try:
        await update_announcement_statuses()

        await db_session.refresh(announcement)
        assert announcement.status == AnnouncementStatus.PRE_REGISTRATION
    finally:
        tasks.announcement_tasks.create_db = original_create_db


@pytest.mark.asyncio
async def test_update_announcement_statuses_pre_registration_to_open(
    db_session, create_user
):
    """Test transition from PRE_REGISTRATION to REGISTRATION_OPEN."""
    user = await create_user(email="organizer1@example.com")
    game = Game(name="Game 1", category="FPS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    announcement = Announcement(
        title="Registration Starting",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        status=AnnouncementStatus.PRE_REGISTRATION,
        registration_start_at=now - timedelta(minutes=1),
        registration_end_at=now + timedelta(hours=1),
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.commit()

    # Mock create_db
    mock_db = MagicMock()
    mock_db.session_factory.return_value.__aenter__.return_value = db_session
    mock_db.session_factory.return_value.__aexit__.return_value = AsyncMock()

    import tasks.announcement_tasks

    original_create_db = tasks.announcement_tasks.create_db
    tasks.announcement_tasks.create_db = lambda: mock_db

    try:
        await update_announcement_statuses()

        await db_session.refresh(announcement)
        assert announcement.status == AnnouncementStatus.REGISTRATION_OPEN
    finally:
        tasks.announcement_tasks.create_db = original_create_db


@pytest.mark.asyncio
async def test_update_announcement_statuses_open_to_closed(db_session, create_user):
    """Test transition from REGISTRATION_OPEN to REGISTRATION_CLOSED."""
    user = await create_user(email="organizer2@example.com")
    game = Game(name="Game 2", category="RPG", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    announcement = Announcement(
        title="Registration Ending",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        status=AnnouncementStatus.REGISTRATION_OPEN,
        registration_start_at=now - timedelta(hours=2),
        registration_end_at=now - timedelta(minutes=1),
        start_at=now + timedelta(hours=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.commit()

    mock_db = MagicMock()
    mock_db.session_factory.return_value.__aenter__.return_value = db_session
    mock_db.session_factory.return_value.__aexit__.return_value = AsyncMock()

    import tasks.announcement_tasks

    original_create_db = tasks.announcement_tasks.create_db
    tasks.announcement_tasks.create_db = lambda: mock_db

    try:
        await update_announcement_statuses()

        await db_session.refresh(announcement)
        assert announcement.status == AnnouncementStatus.REGISTRATION_CLOSED
    finally:
        tasks.announcement_tasks.create_db = original_create_db


@pytest.mark.asyncio
async def test_update_announcement_statuses_closed_to_live(db_session, create_user):
    """Test transition from REGISTRATION_CLOSED to LIVE."""
    user = await create_user(email="organizer3@example.com")
    game = Game(name="Game 3", category="MOBA", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    announcement = Announcement(
        title="Going Live",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
        registration_start_at=now - timedelta(hours=3),
        registration_end_at=now - timedelta(hours=1),
        start_at=now - timedelta(minutes=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.commit()

    mock_db = MagicMock()
    mock_db.session_factory.return_value.__aenter__.return_value = db_session
    mock_db.session_factory.return_value.__aexit__.return_value = AsyncMock()

    import tasks.announcement_tasks

    original_create_db = tasks.announcement_tasks.create_db
    tasks.announcement_tasks.create_db = lambda: mock_db

    try:
        await update_announcement_statuses()

        await db_session.refresh(announcement)
        assert announcement.status == AnnouncementStatus.LIVE
    finally:
        tasks.announcement_tasks.create_db = original_create_db


@pytest.mark.asyncio
async def test_update_announcement_statuses_multiple_transitions(
    db_session, create_user
):
    """Test multiple announcements transitioning simultaneously."""
    user = await create_user(email="organizer4@example.com")
    game = Game(name="Game 4", category="Strategy", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)

    announcement1 = Announcement(
        title="Announcement 1",
        content="Content 1",
        game_id=game.id,
        organizer_id=user.id,
        status=AnnouncementStatus.PRE_REGISTRATION,
        registration_start_at=now - timedelta(minutes=1),
        registration_end_at=now + timedelta(hours=1),
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )

    announcement2 = Announcement(
        title="Announcement 2",
        content="Content 2",
        game_id=game.id,
        organizer_id=user.id,
        status=AnnouncementStatus.REGISTRATION_OPEN,
        registration_start_at=now - timedelta(hours=2),
        registration_end_at=now - timedelta(minutes=1),
        start_at=now + timedelta(hours=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )

    announcement3 = Announcement(
        title="Announcement 3",
        content="Content 3",
        game_id=game.id,
        organizer_id=user.id,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
        registration_start_at=now - timedelta(hours=3),
        registration_end_at=now - timedelta(hours=1),
        start_at=now - timedelta(minutes=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )

    db_session.add_all([announcement1, announcement2, announcement3])
    await db_session.commit()

    mock_db = MagicMock()
    mock_db.session_factory.return_value.__aenter__.return_value = db_session
    mock_db.session_factory.return_value.__aexit__.return_value = AsyncMock()

    import tasks.announcement_tasks

    original_create_db = tasks.announcement_tasks.create_db
    tasks.announcement_tasks.create_db = lambda: mock_db

    try:
        await update_announcement_statuses()

        await db_session.refresh(announcement1)
        await db_session.refresh(announcement2)
        await db_session.refresh(announcement3)

        assert announcement1.status == AnnouncementStatus.REGISTRATION_OPEN
        assert announcement2.status == AnnouncementStatus.REGISTRATION_CLOSED
        assert announcement3.status == AnnouncementStatus.LIVE
    finally:
        tasks.announcement_tasks.create_db = original_create_db


@pytest.mark.asyncio
async def test_update_announcement_statuses_skip_finished_cancelled(
    db_session, create_user
):
    """Test that FINISHED and CANCELLED announcements are not updated."""
    user = await create_user(email="organizer5@example.com")
    game = Game(name="Game 5", category="Puzzle", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)

    announcement_finished = Announcement(
        title="Finished Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        status=AnnouncementStatus.FINISHED,
        registration_start_at=now - timedelta(hours=3),
        registration_end_at=now - timedelta(hours=2),
        start_at=now - timedelta(hours=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )

    announcement_cancelled = Announcement(
        title="Cancelled Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        status=AnnouncementStatus.CANCELLED,
        registration_start_at=now - timedelta(hours=3),
        registration_end_at=now - timedelta(hours=2),
        start_at=now - timedelta(hours=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )

    db_session.add_all([announcement_finished, announcement_cancelled])
    await db_session.commit()

    mock_db = MagicMock()
    mock_db.session_factory.return_value.__aenter__.return_value = db_session
    mock_db.session_factory.return_value.__aexit__.return_value = AsyncMock()

    import tasks.announcement_tasks

    original_create_db = tasks.announcement_tasks.create_db
    tasks.announcement_tasks.create_db = lambda: mock_db

    try:
        await update_announcement_statuses()

        await db_session.refresh(announcement_finished)
        await db_session.refresh(announcement_cancelled)

        assert announcement_finished.status == AnnouncementStatus.FINISHED
        assert announcement_cancelled.status == AnnouncementStatus.CANCELLED
    finally:
        tasks.announcement_tasks.create_db = original_create_db


@pytest.mark.asyncio
async def test_update_announcement_statuses_exact_time_boundary(
    db_session, create_user
):
    """Test transitions at exact time boundaries."""
    user = await create_user(email="organizer6@example.com")
    game = Game(name="Game 6", category="Action", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)

    announcement = Announcement(
        title="Exact Time Test",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        status=AnnouncementStatus.PRE_REGISTRATION,
        registration_start_at=now,
        registration_end_at=now + timedelta(hours=1),
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.commit()

    mock_db = MagicMock()
    mock_db.session_factory.return_value.__aenter__.return_value = db_session
    mock_db.session_factory.return_value.__aexit__.return_value = AsyncMock()

    import tasks.announcement_tasks

    original_create_db = tasks.announcement_tasks.create_db
    tasks.announcement_tasks.create_db = lambda: mock_db

    try:
        await update_announcement_statuses()

        await db_session.refresh(announcement)
        assert announcement.status == AnnouncementStatus.REGISTRATION_OPEN
    finally:
        tasks.announcement_tasks.create_db = original_create_db
