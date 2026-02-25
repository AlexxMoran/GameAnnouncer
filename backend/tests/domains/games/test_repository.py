import pytest
from datetime import datetime, timedelta
from sqlalchemy import select

from domains.games.model import Game
from domains.games.repository import GameRepository
from domains.announcements.model import Announcement
from enums import AnnouncementFormat, SeedMethod


@pytest.mark.asyncio
async def test_save_creates_game(db_session):
    game = Game(name="NewGame", category="RTS", description="d")
    repo = GameRepository(db_session)

    created = await repo.save(game)
    await db_session.commit()

    assert created.id is not None
    assert created.name == "NewGame"


@pytest.mark.asyncio
async def test_find_all_returns_games(db_session):
    g1 = Game(name="AGame", category="RTS", description="x")
    g2 = Game(name="BGame", category="RTS", description="y")
    db_session.add_all([g1, g2])
    await db_session.commit()

    repo = GameRepository(db_session)
    results, total = await repo.find_all(skip=0, limit=10)

    assert any(r.name == "AGame" for r in results)
    assert total >= 2


@pytest.mark.asyncio
async def test_find_by_id_returns_announcements_count(db_session, create_user):
    user = await create_user(email="anncreator@example.com", password="x")
    game = Game(name="CountGame", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    a1 = Announcement(
        title="T1",
        content="c1",
        game_id=game.id,
        organizer_id=user.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    a2 = Announcement(
        title="T2",
        content="c2",
        game_id=game.id,
        organizer_id=user.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add_all([a1, a2])
    await db_session.commit()

    repo = GameRepository(db_session)
    res = await repo.find_by_id(game.id)

    assert res is not None
    assert getattr(res, "announcements_count", 0) >= 2


@pytest.mark.asyncio
async def test_save_updates_game(db_session):
    game = Game(name="UpGame", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    game.name = "UpGameNew"
    repo = GameRepository(db_session)
    updated = await repo.save(game)
    await db_session.commit()

    assert updated.name == "UpGameNew"


@pytest.mark.asyncio
async def test_delete_removes_game(db_session):
    game = Game(name="DelGame", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    repo = GameRepository(db_session)
    await repo.delete(game)
    await db_session.commit()

    res = await db_session.execute(select(Game).where(Game.id == game.id))
    assert res.scalar_one_or_none() is None
