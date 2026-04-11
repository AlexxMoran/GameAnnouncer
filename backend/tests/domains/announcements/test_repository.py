import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy import select

from domains.announcements.model import Announcement
from domains.announcements.repository import AnnouncementRepository
from domains.games.model import Game
from enums import AnnouncementFormat, SeedMethod


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
async def test_save_creates_announcement(db_session, create_user):
    user = await create_user(email="creator1@example.com", password="x")
    game = Game(name="G-create", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, "Create A")
    repo = AnnouncementRepository(db_session)
    created = await repo.save(ann)
    await db_session.commit()

    assert created.id is not None
    assert created.organizer_id == user.id


@pytest.mark.asyncio
async def test_save_updates_announcement(db_session, create_user):
    user = await create_user(email="creator4b@example.com", password="x")
    game = Game(name="G-upd", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, "G1")
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    ann.title = "Updated Title"
    repo = AnnouncementRepository(db_session)
    updated = await repo.save(ann)
    await db_session.commit()

    assert updated.title == "Updated Title"


@pytest.mark.asyncio
async def test_delete_announcement(db_session, create_user):
    user = await create_user(email="creator5@example.com", password="x")
    game = Game(name="G-del", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, "ToDelete")
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    repo = AnnouncementRepository(db_session)
    await repo.delete(ann)
    await db_session.commit()

    result = await db_session.execute(
        select(Announcement).where(Announcement.id == ann.id)
    )
    assert result.scalar_one_or_none() is None
