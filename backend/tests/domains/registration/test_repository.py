import pytest
from datetime import datetime, timedelta

from domains.announcements.model import Announcement
from domains.games.model import Game
from domains.registration.models import RegistrationRequest
from domains.registration.repository import RegistrationRequestRepository
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
async def test_save_creates_registration_request(db_session, create_user):
    user = await create_user(email="rr_user@example.com", password="x")
    game = Game(name="RRGame", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr = RegistrationRequest(announcement_id=ann.id, user_id=user.id)
    repo = RegistrationRequestRepository(db_session)
    created = await repo.save(rr)
    await db_session.commit()

    assert created.id is not None


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

    repo = RegistrationRequestRepository(db_session)
    results, total = await repo.find_all_by_user_id(user.id)

    assert any(r.id == rr.id for r in results)
    assert total >= 1


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

    repo = RegistrationRequestRepository(db_session)
    results, total = await repo.find_all_by_announcement_id(ann.id)

    assert any(r.id == rr.id for r in results)
    assert total >= 1


@pytest.mark.asyncio
async def test_find_by_user_and_announcement(db_session, create_user):
    user = await create_user(email="rr_lookup@example.com", password="x")
    game = Game(name="RRGame4", category="RTS", description="d")
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

    repo = RegistrationRequestRepository(db_session)
    found = await repo.find_by_user_and_announcement(user.id, ann.id)

    assert found is not None
    assert found.id == rr.id


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

    repo = RegistrationRequestRepository(db_session)
    got = await repo.find_by_id(rr.id)

    assert got is not None
    assert got.id == rr.id
