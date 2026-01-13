import pytest
from types import SimpleNamespace
from unittest.mock import patch
from datetime import datetime, timedelta, timezone

from sqlalchemy import insert, select

from api.v1.crud.announcement import announcement_crud
from models.announcement import Announcement
from models.game import Game
from schemas.announcement import AnnouncementCreate, AnnouncementUpdate


@pytest.mark.asyncio
async def test_create_announcement(db_session, create_user):
    user = await create_user(email="creator1@example.com", password="x")
    game = Game(name="G-create", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    a_in = AnnouncementCreate(
        title="Create A",
        content="c",
        game_id=game.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    created = await announcement_crud.create(
        session=db_session, announcement_in=a_in, user=user
    )

    assert created.id is not None
    assert created.organizer_id == user.id

    from models.announcement_participant import AnnouncementParticipant

    await db_session.execute(
        insert(AnnouncementParticipant).values(
            announcement_id=created.id, user_id=user.id
        )
    )
    await db_session.commit()


@pytest.mark.asyncio
async def test_list_and_count_by_game(db_session, create_user):
    user = await create_user(email="creator2@example.com", password="x")
    game = Game(name="G-list", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    a1 = AnnouncementCreate(
        title="L1",
        content="c1",
        game_id=game.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    a2 = AnnouncementCreate(
        title="L2",
        content="c2",
        game_id=game.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participantsgit=10,
    )
    await announcement_crud.create(session=db_session, announcement_in=a1, user=user)
    await announcement_crud.create(session=db_session, announcement_in=a2, user=user)

    from searches.announcement_search import AnnouncementSearch
    from schemas.filters.announcement_filter import AnnouncementFilter

    filters = AnnouncementFilter(game_id=game.id)
    search = AnnouncementSearch(session=db_session, filters=filters)

    results = await search.results()
    assert len(results) >= 2

    total = await search.count()
    assert total >= 2


@pytest.mark.asyncio
async def test_get_by_organizer_and_participant(db_session, create_user):
    user = await create_user(email="creator3@example.com", password="x")
    game = Game(name="G-org", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    a_in = AnnouncementCreate(
        title="Org A",
        content="x",
        game_id=game.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    created = await announcement_crud.create(
        session=db_session, announcement_in=a_in, user=user
    )

    org_results = await announcement_crud.get_all_by_organizer_id(
        session=db_session, organizer_id=user.id
    )
    assert any(r.organizer_id == user.id for r in org_results)

    from models.announcement_participant import AnnouncementParticipant

    await db_session.execute(
        insert(AnnouncementParticipant).values(
            announcement_id=created.id, user_id=user.id
        )
    )
    await db_session.commit()

    part_results = await announcement_crud.get_all_by_participant_id(
        session=db_session, user_id=user.id
    )
    assert any(r.id == created.id for r in part_results)

    participants = await announcement_crud.get_participants_by_announcement_id(
        session=db_session, announcement=SimpleNamespace(id=created.id)
    )
    assert any(p.id == user.id for p in participants)


@pytest.mark.asyncio
async def test_get_by_id_and_update(db_session, create_user):
    user = await create_user(email="creator4@example.com", password="x")
    game = Game(name="G-get", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    a_in = AnnouncementCreate(
        title="G1",
        content="c",
        game_id=game.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    created = await announcement_crud.create(
        session=db_session, announcement_in=a_in, user=user
    )

    got = await announcement_crud.get_by_id(
        session=db_session, announcement_id=created.id
    )
    assert got.id == created.id

    upd = AnnouncementUpdate(title="Updated Title")
    with patch("api.v1.crud.announcement.authorize_action"):
        updated = await announcement_crud.update(
            session=db_session,
            announcement=got,
            announcement_in=upd,
            user=user,
            action="edit",
        )
    assert updated.title == "Updated Title"


@pytest.mark.asyncio
async def test_delete_announcement(db_session, create_user):
    user = await create_user(email="creator5@example.com", password="x")
    game = Game(name="G-del", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    a_in = AnnouncementCreate(
        title="ToDelete",
        content="c",
        game_id=game.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    created = await announcement_crud.create(
        session=db_session, announcement_in=a_in, user=user
    )

    with patch("api.v1.crud.announcement.authorize_action"):
        await announcement_crud.delete(
            session=db_session, announcement=created, user=user, action="delete"
        )

    res = await db_session.execute(
        select(Announcement).where(Announcement.id == created.id)
    )
    assert res.scalar_one_or_none() is None
