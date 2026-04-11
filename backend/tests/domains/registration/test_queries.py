import pytest
from datetime import datetime, timedelta

from domains.announcements.model import Announcement
from domains.games.model import Game
from domains.registration.models import RegistrationRequest
from domains.registration.queries import RegistrationRequestQueries
from enums import AnnouncementFormat, SeedMethod


def _make_announcement(
    game_id: int, organizer_id: int, title: str = "Ann"
) -> Announcement:
    now = datetime.now()
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
async def test_find_all_by_user_id(db_session, create_user):
    user = await create_user(email="rr_user_list@example.com", password="x")
    game = Game(name="RRGame2", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr = RegistrationRequest(announcement_id=ann.id, user_id=user.id)
    db_session.add(rr)
    await db_session.commit()
    await db_session.refresh(rr)

    queries = RegistrationRequestQueries(db_session)
    results, total = await queries.find_all_by_user_id(user.id)

    assert any(result.id == rr.id for result in results)
    assert total >= 1


@pytest.mark.asyncio
async def test_find_all_by_user_id_loads_announcement_game(db_session, create_user):
    user = await create_user(email="rr_user_game@example.com", password="x")
    game = Game(name="GameForUserList", category="FPS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr = RegistrationRequest(announcement_id=ann.id, user_id=user.id)
    db_session.add(rr)
    await db_session.commit()
    await db_session.refresh(rr)

    queries = RegistrationRequestQueries(db_session)
    results, _ = await queries.find_all_by_user_id(user.id)

    found = next(result for result in results if result.id == rr.id)
    assert found.announcement is not None
    assert found.announcement.game is not None
    assert found.announcement.game.id == game.id
    assert found.announcement.game.name == "GameForUserList"


@pytest.mark.asyncio
async def test_find_all_by_announcement_id(db_session, create_user):
    user = await create_user(email="rr_ann_list@example.com", password="x")
    game = Game(name="RRGame3", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr = RegistrationRequest(announcement_id=ann.id, user_id=user.id)
    db_session.add(rr)
    await db_session.commit()
    await db_session.refresh(rr)

    queries = RegistrationRequestQueries(db_session)
    results, total = await queries.find_all_by_announcement_id(ann.id)

    assert any(result.id == rr.id for result in results)
    assert total >= 1


@pytest.mark.asyncio
async def test_find_all_by_announcement_id_loads_announcement_game(
    db_session, create_user
):
    user = await create_user(email="rr_ann_game@example.com", password="x")
    game = Game(name="GameForAnnList", category="MOBA", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr = RegistrationRequest(announcement_id=ann.id, user_id=user.id)
    db_session.add(rr)
    await db_session.commit()
    await db_session.refresh(rr)

    queries = RegistrationRequestQueries(db_session)
    results, _ = await queries.find_all_by_announcement_id(ann.id)

    found = next(result for result in results if result.id == rr.id)
    assert found.announcement is not None
    assert found.announcement.game is not None
    assert found.announcement.game.id == game.id


@pytest.mark.asyncio
async def test_find_by_id_loads_relations(db_session, create_user):
    user = await create_user(email="rr_byid@example.com", password="x")
    game = Game(name="RRGame5", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr = RegistrationRequest(announcement_id=ann.id, user_id=user.id)
    db_session.add(rr)
    await db_session.commit()
    await db_session.refresh(rr)

    queries = RegistrationRequestQueries(db_session)
    got = await queries.find_by_id(rr.id)

    assert got is not None
    assert got.id == rr.id
    assert got.announcement is not None
    assert got.announcement.game is not None
    assert got.announcement.game.id == game.id
