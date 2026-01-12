import pytest
from datetime import datetime, timedelta, timezone

from searches.announcement_search import AnnouncementSearch
from schemas.filters.announcement_filter import AnnouncementFilter
from models.announcement import Announcement
from models.game import Game


@pytest.mark.asyncio
async def test_announcement_search_model_and_filter_schema():
    """Test that AnnouncementSearch has correct model and filter_schema"""
    assert AnnouncementSearch.model == Announcement
    assert AnnouncementSearch.filter_schema == AnnouncementFilter


@pytest.mark.asyncio
async def test_announcement_search_no_filters(db_session, create_user):
    """Test search with no filters returns all announcements"""
    user = await create_user(email="search1@example.com", password="x")
    game = Game(name="SearchGame1", category="Action", description="test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    ann1 = Announcement(
        title="Ann1",
        content="content1",
        game_id=game.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
    )
    ann2 = Announcement(
        title="Ann2",
        content="content2",
        game_id=game.id,
        organizer_id=user.id,
        status="registration_open",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
    )
    db_session.add_all([ann1, ann2])
    await db_session.commit()

    filters = AnnouncementFilter()
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert len(results) >= 2
    assert count >= 2


@pytest.mark.asyncio
async def test_announcement_search_filter_by_game_id(db_session, create_user):
    """Test filtering announcements by game_id"""
    user = await create_user(email="search2@example.com", password="x")

    game1 = Game(name="Game1", category="Action", description="test1")
    game2 = Game(name="Game2", category="RPG", description="test2")
    db_session.add_all([game1, game2])
    await db_session.commit()
    await db_session.refresh(game1)
    await db_session.refresh(game2)

    now = datetime.now(timezone.utc)
    ann1 = Announcement(
        title="Game1Ann",
        content="content1",
        game_id=game1.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
    )
    ann2 = Announcement(
        title="Game2Ann",
        content="content2",
        game_id=game2.id,
        organizer_id=user.id,
        status="registration_open",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
    )
    db_session.add_all([ann1, ann2])
    await db_session.commit()

    # Search for game1 announcements only
    filters = AnnouncementFilter(game_id=game1.id)
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert all(ann.game_id == game1.id for ann in results)
    assert count >= 1
    assert any(ann.title == "Game1Ann" for ann in results)


@pytest.mark.asyncio
async def test_announcement_search_filter_by_status(db_session, create_user):
    """Test filtering announcements by status"""
    user = await create_user(email="search3@example.com", password="x")
    game = Game(name="StatusGame", category="Strategy", description="test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    ann1 = Announcement(
        title="PreRegAnn",
        content="content1",
        game_id=game.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
    )
    ann2 = Announcement(
        title="LiveAnn",
        content="content2",
        game_id=game.id,
        organizer_id=user.id,
        status="live",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
    )
    db_session.add_all([ann1, ann2])
    await db_session.commit()

    # Search for only "live" status
    filters = AnnouncementFilter(status="live")
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert all(ann.status == "live" for ann in results)
    assert count >= 1
    assert any(ann.title == "LiveAnn" for ann in results)


@pytest.mark.asyncio
async def test_announcement_search_filter_by_game_and_status(db_session, create_user):
    """Test filtering announcements by both game_id and status"""
    user = await create_user(email="search4@example.com", password="x")

    game1 = Game(name="MultiGame1", category="Action", description="test1")
    game2 = Game(name="MultiGame2", category="RPG", description="test2")
    db_session.add_all([game1, game2])
    await db_session.commit()
    await db_session.refresh(game1)
    await db_session.refresh(game2)

    now = datetime.now(timezone.utc)

    ann1 = Announcement(
        title="G1PreReg",
        content="content1",
        game_id=game1.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
    )

    ann2 = Announcement(
        title="G1Live",
        content="content2",
        game_id=game1.id,
        organizer_id=user.id,
        status="live",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
    )

    ann3 = Announcement(
        title="G2PreReg",
        content="content3",
        game_id=game2.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
    )

    db_session.add_all([ann1, ann2, ann3])
    await db_session.commit()

    filters = AnnouncementFilter(game_id=game1.id, status="pre_registration")
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert all(ann.game_id == game1.id for ann in results)
    assert all(ann.status == "pre_registration" for ann in results)
    assert count >= 1
    assert any(ann.title == "G1PreReg" for ann in results)


@pytest.mark.asyncio
async def test_announcement_search_pagination(db_session, create_user):
    """Test pagination with skip and limit"""
    user = await create_user(email="search5@example.com", password="x")
    game = Game(name="PaginationGame", category="Sports", description="test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    announcements = []
    for i in range(5):
        ann = Announcement(
            title=f"Ann{i}",
            content=f"content{i}",
            game_id=game.id,
            organizer_id=user.id,
            status="pre_registration",
            start_at=now + timedelta(days=30),
            registration_start_at=now + timedelta(days=1),
            registration_end_at=now + timedelta(days=29),
        )
        announcements.append(ann)

    db_session.add_all(announcements)
    await db_session.commit()

    filters = AnnouncementFilter(game_id=game.id)
    search = AnnouncementSearch(session=db_session, filters=filters)

    page1 = await search.results(skip=0, limit=2)
    assert len(page1) == 2

    page2 = await search.results(skip=2, limit=2)
    assert len(page2) == 2

    page1_ids = {ann.id for ann in page1}
    page2_ids = {ann.id for ann in page2}
    assert page1_ids.isdisjoint(page2_ids)

    total = await search.count()
    assert total >= 5


@pytest.mark.asyncio
async def test_announcement_search_count_matches_results(db_session, create_user):
    """Test that count() returns the same number as len(results())"""
    user = await create_user(email="search6@example.com", password="x")
    game = Game(name="CountGame", category="Puzzle", description="test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    for i in range(3):
        ann = Announcement(
            title=f"CountAnn{i}",
            content=f"content{i}",
            game_id=game.id,
            organizer_id=user.id,
            status="registration_open",
            start_at=now + timedelta(days=30),
            registration_start_at=now + timedelta(days=1),
            registration_end_at=now + timedelta(days=29),
        )
        db_session.add(ann)

    await db_session.commit()

    filters = AnnouncementFilter(game_id=game.id, status="registration_open")
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results(skip=0, limit=100)
    count = await search.count()

    game_results = [r for r in results if r.game_id == game.id]
    assert len(game_results) == count


@pytest.mark.asyncio
async def test_announcement_search_empty_results(db_session, create_user):
    """Test search returns empty when no matches found"""
    await create_user(email="search7@example.com", password="x")

    filters = AnnouncementFilter(game_id=999999)
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert len(results) == 0
    assert count == 0


@pytest.mark.asyncio
async def test_announcement_search_base_query_returns_query(db_session):
    """Test that base_query() returns a valid SQLAlchemy query"""
    filters = AnnouncementFilter()
    search = AnnouncementSearch(session=db_session, filters=filters)

    query = search.base_query()

    assert hasattr(query, "whereclause")


@pytest.mark.asyncio
async def test_announcement_search_inherits_from_base_search(db_session):
    """Test that AnnouncementSearch properly inherits from BaseSearch"""
    filters = AnnouncementFilter()
    search = AnnouncementSearch(session=db_session, filters=filters)

    assert hasattr(search, "base_query")
    assert hasattr(search, "apply_filters")
    assert hasattr(search, "results")
    assert hasattr(search, "count")
    assert search.session == db_session
    assert search.filters == filters
