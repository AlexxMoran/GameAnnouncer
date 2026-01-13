import pytest
from sqlalchemy import select
from unittest.mock import patch
from datetime import datetime, timedelta

from models.game import Game
from models.announcement import Announcement
from schemas.game import GameCreate, GameUpdate
from api.v1.crud.game import game_crud


@pytest.mark.asyncio
async def test_create_game(db_session, create_user):
    user = await create_user(email="gcreator@example.com", password="x")

    g_in = GameCreate(name="NewGame", category="RTS", description="d")

    with patch("api.v1.crud.game.authorize_action"):
        created = await game_crud.create(
            session=db_session, game_in=g_in, user=user, action="create"
        )

    assert created.id is not None
    assert created.name == "NewGame"


@pytest.mark.asyncio
async def test_get_all_and_count(db_session):
    g1 = Game(name="AGame", category="RTS", description="x")
    g2 = Game(name="BGame", category="RTS", description="y")
    db_session.add_all([g1, g2])
    await db_session.commit()

    results = await game_crud.get_all(session=db_session, skip=0, limit=10)
    assert any(r.name == "AGame" for r in results)

    total = await game_crud.get_all_count(session=db_session)
    assert total >= 2


@pytest.mark.asyncio
async def test_get_by_id_with_announcements_count(db_session, create_user):
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
    )
    db_session.add_all([a1, a2])
    await db_session.commit()

    res = await game_crud.get_by_id(session=db_session, game_id=game.id)
    assert res is not None
    assert getattr(res, "announcements_count", 0) >= 2


@pytest.mark.asyncio
async def test_update_game(db_session, create_user):
    user = await create_user(email="updater@example.com", password="x")
    game = Game(name="UpGame", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    upd = GameUpdate(name="UpGameNew")
    with patch("api.v1.crud.game.authorize_action"):
        updated = await game_crud.update(
            session=db_session, game=game, game_in=upd, user=user, action="edit"
        )

    assert updated.name == "UpGameNew"


@pytest.mark.asyncio
async def test_delete_game(db_session, create_user):
    user = await create_user(email="delg@example.com", password="x")
    game = Game(name="DelGame", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    with patch("api.v1.crud.game.authorize_action"):
        await game_crud.delete(
            session=db_session, game=game, user=user, action="delete"
        )

    res = await db_session.execute(select(Game).where(Game.id == game.id))
    assert res.scalar_one_or_none() is None
