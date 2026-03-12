import pytest
from datetime import datetime, timedelta
from domains.announcements.model import Announcement
from domains.games.model import Game
from exceptions import ValidationException
from enums import AnnouncementFormat, SeedMethod


def test_announcement_table_and_columns():
    assert Announcement.__tablename__ == "announcements"
    cols = Announcement.__table__.columns
    assert "title" in cols
    assert "content" in cols
    assert "image_url" in cols
    assert "game_id" in cols
    assert "organizer_id" in cols
    assert "start_at" in cols
    assert "registration_start_at" in cols
    assert "registration_end_at" in cols
    assert "max_participants" in cols
    assert "status" in cols
    assert "format" in cols


def test_announcement_relationships():
    rels = {r.key for r in Announcement.__mapper__.relationships}
    assert "organizer" in rels
    assert "game" in rels
    assert "participants" in rels
    assert "registration_requests" in rels


@pytest.mark.asyncio
async def test_valid_dates_order(db_session, create_user):
    user = await create_user(email="valid@example.com", password="x")
    game = Game(name="ValidGame", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    ann = Announcement(
        title="Valid",
        content="c",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        start_at=now + timedelta(days=30),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(ann)
    await db_session.commit()

    assert ann.id is not None


@pytest.mark.asyncio
async def test_start_equals_registration_end(db_session, create_user):
    user = await create_user(email="equal@example.com", password="x")
    game = Game(name="EqualGame", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    ann = Announcement(
        title="Equal",
        content="c",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        start_at=now + timedelta(days=29),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(ann)
    await db_session.commit()

    assert ann.id is not None


@pytest.mark.asyncio
async def test_invalid_start_before_registration_end(db_session, create_user):
    user = await create_user(email="invalid1@example.com", password="x")
    game = Game(name="Invalid1", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    with pytest.raises(ValidationException) as exc_info:
        Announcement(
            title="Invalid",
            content="c",
            game_id=game.id,
            organizer_id=user.id,
            registration_start_at=now,
            registration_end_at=now + timedelta(days=30),
            start_at=now + timedelta(days=29),
            max_participants=10,
            format=AnnouncementFormat.SINGLE_ELIMINATION,
            has_qualification=False,
            seed_method=SeedMethod.RANDOM,
        )

    assert "start_at must be after or equal to registration_end_at" in str(
        exc_info.value
    )


@pytest.mark.asyncio
async def test_invalid_registration_start_equals_end(db_session, create_user):
    user = await create_user(email="invalid2@example.com", password="x")
    game = Game(name="Invalid2", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    with pytest.raises(ValidationException) as exc_info:
        Announcement(
            title="Invalid",
            content="c",
            game_id=game.id,
            organizer_id=user.id,
            registration_start_at=now,
            registration_end_at=now,
            start_at=now + timedelta(days=1),
            max_participants=10,
            format=AnnouncementFormat.SINGLE_ELIMINATION,
            has_qualification=False,
            seed_method=SeedMethod.RANDOM,
        )

    assert "registration_start_at must be before registration_end_at" in str(
        exc_info.value
    )


@pytest.mark.asyncio
async def test_invalid_registration_start_after_end(db_session, create_user):
    user = await create_user(email="invalid3@example.com", password="x")
    game = Game(name="Invalid3", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    with pytest.raises(ValidationException) as exc_info:
        Announcement(
            title="Invalid",
            content="c",
            game_id=game.id,
            organizer_id=user.id,
            registration_start_at=now + timedelta(days=30),
            registration_end_at=now + timedelta(days=29),
            start_at=now + timedelta(days=31),
            max_participants=10,
            format=AnnouncementFormat.SINGLE_ELIMINATION,
            has_qualification=False,
            seed_method=SeedMethod.RANDOM,
        )

    assert "registration_start_at must be before registration_end_at" in str(
        exc_info.value
    )


@pytest.mark.asyncio
async def test_is_registration_open_during_period(db_session, create_user):
    """Test that is_registration_open returns True during registration period."""
    user = await create_user(email="open@example.com")
    game = Game(name="Open Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Open Registration",
        content="c",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now - timedelta(hours=1),
        registration_end_at=now + timedelta(hours=1),
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    assert announcement.is_registration_open is True


@pytest.mark.asyncio
async def test_is_registration_open_before_start(db_session, create_user):
    """Test that is_registration_open returns False before registration starts."""
    user = await create_user(email="before@example.com")
    game = Game(name="Before Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Before Registration",
        content="c",
        game_id=game.id,
        organizer_id=user.id,
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
    await db_session.refresh(announcement)

    assert announcement.is_registration_open is False


@pytest.mark.asyncio
async def test_valid_announcement_format(db_session, create_user):
    """Test that announcement can be created with valid format."""
    user = await create_user(email="format_valid@example.com", password="x")
    game = Game(name="FormatGame", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Valid Format",
        content="Test content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now,
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    assert announcement.id is not None
    assert announcement.format == AnnouncementFormat.SINGLE_ELIMINATION


@pytest.mark.asyncio
async def test_announcement_format_string_value(db_session, create_user):
    """Test that announcement format can be set using string value."""
    user = await create_user(email="format_string@example.com", password="x")
    game = Game(name="StringFormatGame", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="String Format",
        content="Test content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now,
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
        format="SINGLE_ELIMINATION",
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    assert announcement.id is not None
    assert announcement.format == AnnouncementFormat.SINGLE_ELIMINATION
