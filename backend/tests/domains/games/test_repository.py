import pytest
from sqlalchemy import select

from domains.games.model import Game
from domains.games.repository import GameRepository


@pytest.mark.asyncio
async def test_save_creates_game(db_session):
    game = Game(name="NewGame", category="RTS", description="d")
    repo = GameRepository(db_session)

    created = await repo.save(game)
    await db_session.commit()

    assert created.id is not None
    assert created.name == "NewGame"


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

    result = await db_session.execute(select(Game).where(Game.id == game.id))
    assert result.scalar_one_or_none() is None
