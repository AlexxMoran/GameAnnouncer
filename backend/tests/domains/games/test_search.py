import pytest

from domains.games.search import GameSearch
from domains.games.schemas import GameFilter
from domains.games.model import Game


@pytest.mark.asyncio
async def test_game_search_model_and_filter_schema():
    assert GameSearch.model == Game
    assert GameSearch.filter_schema == GameFilter


@pytest.mark.asyncio
async def test_game_search_no_filters(db_session):
    game1 = Game(name="Test Game 1", category="Action", description="First test game")
    game2 = Game(name="Test Game 2", category="RPG", description="Second test game")
    db_session.add_all([game1, game2])
    await db_session.commit()

    filters = GameFilter()
    search = GameSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.filtered_count()

    assert len(results) >= 2
    assert count >= 2


@pytest.mark.asyncio
async def test_game_search_filter_by_name_exact(db_session):
    game1 = Game(name="Dota 2", category="MOBA", description="test1")
    game2 = Game(name="Counter-Strike", category="FPS", description="test2")
    db_session.add_all([game1, game2])
    await db_session.commit()

    filters = GameFilter(name="Dota 2")
    search = GameSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.filtered_count()

    assert count >= 1
    assert any(game.name == "Dota 2" for game in results)


@pytest.mark.asyncio
async def test_game_search_filter_by_name_partial(db_session):
    game1 = Game(name="Dota 2", category="MOBA", description="test1")
    game2 = Game(name="Dota 1", category="MOBA", description="test2")
    game3 = Game(name="Counter-Strike", category="FPS", description="test3")
    db_session.add_all([game1, game2, game3])
    await db_session.commit()

    filters = GameFilter(name="dota")
    search = GameSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.filtered_count()

    assert count >= 2
    assert all("dota" in game.name.lower() for game in results)


@pytest.mark.asyncio
async def test_game_search_pagination(db_session):
    games = [
        Game(name=f"PaginationGame{i}", category="Puzzle", description=f"test{i}")
        for i in range(5)
    ]
    db_session.add_all(games)
    await db_session.commit()

    filters = GameFilter()
    search = GameSearch(session=db_session, filters=filters)

    page1 = await search.results(skip=0, limit=2)
    page2 = await search.results(skip=2, limit=2)

    assert len(page1) == 2
    assert len(page2) == 2
    assert {g.id for g in page1}.isdisjoint({g.id for g in page2})
    assert await search.filtered_count() >= 5


@pytest.mark.asyncio
async def test_game_search_empty_results(db_session):
    filters = GameFilter(name="NonExistentGame12345")
    search = GameSearch(session=db_session, filters=filters)

    assert len(await search.results()) == 0
    assert await search.filtered_count() == 0
