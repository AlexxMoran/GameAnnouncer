import pytest

from searches.game_search import GameSearch
from schemas.filters.game_filter import GameFilter
from models.game import Game


@pytest.mark.asyncio
async def test_game_search_model_and_filter_schema():
    """Test that GameSearch has correct model and filter_schema"""
    assert GameSearch.model == Game
    assert GameSearch.filter_schema == GameFilter


@pytest.mark.asyncio
async def test_game_search_no_filters(db_session):
    """Test search with no filters returns all games"""
    game1 = Game(name="Test Game 1", category="Action", description="First test game")
    game2 = Game(name="Test Game 2", category="RPG", description="Second test game")
    db_session.add_all([game1, game2])
    await db_session.commit()

    filters = GameFilter()
    search = GameSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert len(results) >= 2
    assert count >= 2


@pytest.mark.asyncio
async def test_game_search_filter_by_name_exact(db_session):
    """Test filtering games by exact name"""
    game1 = Game(name="Dota 2", category="MOBA", description="test1")
    game2 = Game(name="Counter-Strike", category="FPS", description="test2")
    db_session.add_all([game1, game2])
    await db_session.commit()

    filters = GameFilter(name="Dota 2")
    search = GameSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert count >= 1
    assert any(game.name == "Dota 2" for game in results)
    assert all("Dota" in game.name or "dota" in game.name.lower() for game in results)


@pytest.mark.asyncio
async def test_game_search_filter_by_name_partial(db_session):
    """Test filtering games by partial name (ILIKE)"""
    game1 = Game(name="Dota 2", category="MOBA", description="test1")
    game2 = Game(name="Dota 1", category="MOBA", description="test2")
    game3 = Game(name="Counter-Strike", category="FPS", description="test3")
    db_session.add_all([game1, game2, game3])
    await db_session.commit()

    # Search for "dota" should find both Dota games
    filters = GameFilter(name="dota")
    search = GameSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert count >= 2
    assert all("dota" in game.name.lower() for game in results)
    assert any(game.name == "Dota 2" for game in results)
    assert any(game.name == "Dota 1" for game in results)


@pytest.mark.asyncio
async def test_game_search_filter_by_name_case_insensitive(db_session):
    """Test that name filtering is case-insensitive"""
    game1 = Game(name="League of Legends", category="MOBA", description="test")
    game2 = Game(name="LEAGUE Online", category="RPG", description="test2")
    db_session.add_all([game1, game2])
    await db_session.commit()

    # Lowercase search should find games with uppercase
    filters = GameFilter(name="league")
    search = GameSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert count >= 2
    assert all("league" in game.name.lower() for game in results)


@pytest.mark.asyncio
async def test_game_search_filter_by_name_partial_match(db_session):
    """Test filtering with partial name like 'do' finds 'Dota 2'"""
    game1 = Game(name="Dota 2", category="MOBA", description="test1")
    game2 = Game(name="Shadow of Mordor", category="Action", description="test2")
    game3 = Game(name="Counter-Strike", category="FPS", description="test3")
    db_session.add_all([game1, game2, game3])
    await db_session.commit()

    # Search for "do" should find both "Dota" and "Mordor"
    filters = GameFilter(name="do")
    search = GameSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert count >= 2
    assert any(game.name == "Dota 2" for game in results)
    assert any(game.name == "Shadow of Mordor" for game in results)


@pytest.mark.asyncio
async def test_game_search_pagination(db_session):
    """Test pagination with skip and limit"""
    games = []
    for i in range(5):
        game = Game(
            name=f"PaginationGame{i}",
            category="Puzzle",
            description=f"test{i}",
        )
        games.append(game)

    db_session.add_all(games)
    await db_session.commit()

    filters = GameFilter()
    search = GameSearch(session=db_session, filters=filters)

    page1 = await search.results(skip=0, limit=2)
    assert len(page1) == 2

    page2 = await search.results(skip=2, limit=2)
    assert len(page2) == 2

    page1_ids = {game.id for game in page1}
    page2_ids = {game.id for game in page2}
    assert page1_ids.isdisjoint(page2_ids)

    total = await search.count()
    assert total >= 5


@pytest.mark.asyncio
async def test_game_search_count_matches_results(db_session):
    """Test that count() returns the same number as len(results())"""
    for i in range(3):
        game = Game(
            name=f"CountGame{i}",
            category="Strategy",
            description=f"content{i}",
        )
        db_session.add(game)

    await db_session.commit()

    filters = GameFilter(name="CountGame")
    search = GameSearch(session=db_session, filters=filters)

    results = await search.results(skip=0, limit=100)
    count = await search.count()

    filtered_results = [r for r in results if "CountGame" in r.name]
    assert len(filtered_results) == count


@pytest.mark.asyncio
async def test_game_search_empty_results(db_session):
    """Test search returns empty when no matches found"""
    filters = GameFilter(name="NonExistentGame12345")
    search = GameSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert len(results) == 0
    assert count == 0


@pytest.mark.asyncio
async def test_game_search_base_query_returns_query(db_session):
    """Test that base_query() returns a valid SQLAlchemy query"""
    filters = GameFilter()
    search = GameSearch(session=db_session, filters=filters)

    query = search.base_query()

    assert hasattr(query, "whereclause")


@pytest.mark.asyncio
async def test_game_search_inherits_from_base_search(db_session):
    """Test that GameSearch properly inherits from BaseSearch"""
    filters = GameFilter()
    search = GameSearch(session=db_session, filters=filters)

    assert hasattr(search, "base_query")
    assert hasattr(search, "apply_filters")
    assert hasattr(search, "results")
    assert hasattr(search, "count")
    assert search.session == db_session
    assert search.filters == filters


@pytest.mark.asyncio
async def test_game_search_name_with_special_characters(db_session):
    """Test that search handles special SQL characters safely"""
    game = Game(name="Game%With_Special", category="Action", description="test")
    db_session.add(game)
    await db_session.commit()

    # These should be escaped properly and not cause SQL errors
    filters = GameFilter(name="%")
    search = GameSearch(session=db_session, filters=filters)
    results = await search.results()

    # Should find game with % in name
    assert any("%" in game.name for game in results)


@pytest.mark.asyncio
async def test_game_search_with_multiple_partial_matches(db_session):
    """Test that partial search returns all matching games"""
    game1 = Game(name="Battle Royale", category="Action", description="test1")
    game2 = Game(name="Battle Arena", category="MOBA", description="test2")
    game3 = Game(name="Chess Battle", category="Strategy", description="test3")
    game4 = Game(name="Racing Game", category="Racing", description="test4")
    db_session.add_all([game1, game2, game3, game4])
    await db_session.commit()

    filters = GameFilter(name="battle")
    search = GameSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert count == 3
    assert all("battle" in game.name.lower() for game in results)
    assert any(game.name == "Battle Royale" for game in results)
    assert any(game.name == "Battle Arena" for game in results)
    assert any(game.name == "Chess Battle" for game in results)
