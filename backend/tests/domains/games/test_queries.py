import pytest
from datetime import datetime, timedelta

from domains.announcements.model import Announcement
from domains.games.model import Game
from domains.games.queries import GameQueries
from enums import AnnouncementFormat, SeedMethod


@pytest.mark.asyncio
async def test_get_by_id_returns_announcements_count(db_session, create_user):
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

    queries = GameQueries(db_session)
    result = await queries.find_by_id(game.id)

    assert result is not None
    assert getattr(result, "announcements_count", 0) >= 2
