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
        max_participants=10,
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
        max_participants=10,
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
        max_participants=10,
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
        max_participants=10,
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
        max_participants=10,
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
        max_participants=10,
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
        max_participants=10,
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
        max_participants=10,
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
        max_participants=10,
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
            max_participants=10,
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
            max_participants=10,
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


@pytest.mark.asyncio
async def test_announcement_search_filter_by_q_finds_game_name(db_session, create_user):
    """Test that search query finds announcements by game name"""
    user = await create_user(email="search_q1@example.com", password="x")

    game_dota = Game(name="Dota 2", category="MOBA", description="Strategy game")
    game_cs = Game(
        name="Counter-Strike", category="FPS", description="Tactical shooter"
    )
    db_session.add_all([game_dota, game_cs])
    await db_session.commit()
    await db_session.refresh(game_dota)
    await db_session.refresh(game_cs)

    now = datetime.now(timezone.utc)
    ann_dota = Announcement(
        title="Weekly Tournament",
        content="Join our tournament",
        game_id=game_dota.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    ann_cs = Announcement(
        title="Weekly Tournament",
        content="Join our tournament",
        game_id=game_cs.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    db_session.add_all([ann_dota, ann_cs])
    await db_session.commit()

    filters = AnnouncementFilter(q="dota")
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert count == 1
    assert len(results) == 1
    assert results[0].game.name == "Dota 2"


@pytest.mark.asyncio
async def test_announcement_search_filter_by_q_finds_title(db_session, create_user):
    """Test that search query finds announcements by title"""
    user = await create_user(email="search_q2@example.com", password="x")

    game = Game(name="TestGame", category="Action", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    ann1 = Announcement(
        title="Championship Finals",
        content="Regular content",
        game_id=game.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    ann2 = Announcement(
        title="Regular Tournament",
        content="Regular content",
        game_id=game.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    db_session.add_all([ann1, ann2])
    await db_session.commit()

    filters = AnnouncementFilter(q="championship")
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert count == 1
    assert len(results) == 1
    assert "Championship" in results[0].title


@pytest.mark.asyncio
async def test_announcement_search_filter_by_q_finds_content(db_session, create_user):
    """Test that search query finds announcements by content"""
    user = await create_user(email="search_q3@example.com", password="x")

    game = Game(name="TestGame", category="Action", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    ann1 = Announcement(
        title="Event 1",
        content="Special prize pool for winners",
        game_id=game.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    ann2 = Announcement(
        title="Event 2",
        content="Join and have fun",
        game_id=game.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    db_session.add_all([ann1, ann2])
    await db_session.commit()

    filters = AnnouncementFilter(q="prize")
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert count == 1
    assert len(results) == 1
    assert "prize" in results[0].content.lower()


@pytest.mark.asyncio
async def test_announcement_search_filter_by_q_case_insensitive(
    db_session, create_user
):
    """Test that search query is case-insensitive"""
    user = await create_user(email="search_q4@example.com", password="x")

    game = Game(name="VALORANT", category="FPS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    ann = Announcement(
        title="Tournament",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    db_session.add(ann)
    await db_session.commit()

    filters = AnnouncementFilter(q="valorant")
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()
    assert len(results) == 1


@pytest.mark.asyncio
async def test_announcement_search_filter_by_q_priority_game_name_first(
    db_session, create_user
):
    """Test that results are prioritized: game.name > title > content"""
    user = await create_user(email="search_q5@example.com", password="x")

    game_league = Game(name="League of Legends", category="MOBA", description="Test")
    game_other = Game(name="Other Game", category="Action", description="Test")
    db_session.add_all([game_league, game_other])
    await db_session.commit()
    await db_session.refresh(game_league)
    await db_session.refresh(game_other)

    now = datetime.now(timezone.utc)

    ann_game_match = Announcement(
        title="Tournament Event",
        content="Join us",
        game_id=game_league.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
        created_at=now - timedelta(hours=2),
    )

    ann_title_match = Announcement(
        title="League Tournament",
        content="Join us",
        game_id=game_other.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
        created_at=now - timedelta(hours=1),
    )

    ann_content_match = Announcement(
        title="Tournament Event",
        content="Best league players",
        game_id=game_other.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
        created_at=now,
    )

    db_session.add_all([ann_game_match, ann_title_match, ann_content_match])
    await db_session.commit()

    filters = AnnouncementFilter(q="league")
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()

    assert len(results) == 3
    assert results[0].game.name == "League of Legends"
    assert "League" in results[1].title
    assert "league" in results[2].content.lower()


@pytest.mark.asyncio
async def test_announcement_search_filter_by_q_min_length(db_session, create_user):
    """Test that search query with less than MIN_SEARCH_LENGTH characters is ignored"""
    user = await create_user(email="search_q6@example.com", password="x")

    game = Game(name="A", category="Action", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    ann = Announcement(
        title="Tournament",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    db_session.add(ann)
    await db_session.commit()

    filters = AnnouncementFilter(q="A")
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()

    assert len(results) >= 1


@pytest.mark.asyncio
async def test_announcement_search_filter_by_q_no_results(db_session, create_user):
    """Test that search query returns empty results when no matches"""
    user = await create_user(email="search_q7@example.com", password="x")

    game = Game(name="TestGame", category="Action", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    ann = Announcement(
        title="Tournament",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    db_session.add(ann)
    await db_session.commit()

    filters = AnnouncementFilter(q="nonexistent")
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert len(results) == 0
    assert count == 0


@pytest.mark.asyncio
async def test_announcement_search_filter_by_q_combined_with_other_filters(
    db_session, create_user
):
    """Test that search query works in combination with other filters"""
    user = await create_user(email="search_q8@example.com", password="x")

    game1 = Game(name="Game One", category="Action", description="Test")
    game2 = Game(name="Game Two", category="RPG", description="Test")
    db_session.add_all([game1, game2])
    await db_session.commit()
    await db_session.refresh(game1)
    await db_session.refresh(game2)

    now = datetime.now(timezone.utc)

    ann1 = Announcement(
        title="Tournament Event",
        content="Content",
        game_id=game1.id,
        organizer_id=user.id,
        status="live",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )

    ann2 = Announcement(
        title="Tournament Event",
        content="Content",
        game_id=game2.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )

    db_session.add_all([ann1, ann2])
    await db_session.commit()

    filters = AnnouncementFilter(q="tournament", status="live")
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert count == 1
    assert len(results) == 1
    assert results[0].status == "live"
    assert "Tournament" in results[0].title


@pytest.mark.asyncio
async def test_announcement_search_sorted_by_created_at_desc_by_default(
    db_session, create_user
):
    """Test that results are sorted by created_at DESC when no search query"""
    user = await create_user(email="search_sort1@example.com", password="x")

    game = Game(name="SortGame", category="Action", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)

    ann_old = Announcement(
        title="Old Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
        created_at=now - timedelta(hours=2),
    )

    ann_new = Announcement(
        title="New Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
        created_at=now,
    )

    db_session.add_all([ann_old, ann_new])
    await db_session.commit()

    filters = AnnouncementFilter()
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()

    game_results = [r for r in results if r.game_id == game.id]
    assert len(game_results) == 2
    assert game_results[0].created_at > game_results[1].created_at


@pytest.mark.asyncio
async def test_announcement_search_filter_by_q_handles_null_content(
    db_session, create_user
):
    """Test that search query handles announcements with NULL content gracefully"""
    user = await create_user(email="search_null1@example.com", password="x")

    game = Game(name="NullGame", category="Action", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)

    ann_with_content = Announcement(
        title="Tournament",
        content="Great tournament event",
        game_id=game.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )

    ann_null_content = Announcement(
        title="Event",
        content=None,
        game_id=game.id,
        organizer_id=user.id,
        status="pre_registration",
        start_at=now + timedelta(days=30),
        registration_start_at=now + timedelta(days=1),
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )

    db_session.add_all([ann_with_content, ann_null_content])
    await db_session.commit()

    filters = AnnouncementFilter(q="tournament")
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()
    count = await search.count()

    assert count == 1
    assert len(results) == 1
    assert results[0].content == "Great tournament event"
