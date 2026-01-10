import pytest
from datetime import datetime, timedelta
from models.announcement import Announcement
from models.game import Game
from exceptions import ValidationException


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
        )

    assert "registration_start_at must be before registration_end_at" in str(
        exc_info.value
    )


@pytest.mark.asyncio
async def test_invalid_all_dates_equal(db_session, create_user):
    user = await create_user(email="invalid4@example.com", password="x")
    game = Game(name="Invalid4", category="RTS", description="d")
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
            start_at=now,
        )

    assert "registration_start_at must be before registration_end_at" in str(
        exc_info.value
    )
