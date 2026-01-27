import pytest
from unittest.mock import patch
from sqlalchemy import select
from datetime import datetime, timedelta

from models.game import Game
from models.announcement import Announcement
from models.registration_request import RegistrationRequest
from enums.registration_status import RegistrationStatus
from api.v1.crud.registration_request import registration_request_crud
from schemas.registration_request import RegistrationRequestCreate


@pytest.mark.asyncio
async def test_create_registration_request(db_session, create_user):
    user = await create_user(email="rr_user@example.com", password="x")
    game = Game(name="RRGame", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    ann = Announcement(
        title="Ann1",
        content="c",
        game_id=game.id,
        organizer_id=user.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr_in = RegistrationRequestCreate(announcement_id=ann.id)
    created = await registration_request_crud.create(
        session=db_session, registration_request_in=rr_in, user=user
    )

    assert created.id is not None


@pytest.mark.asyncio
async def test_get_all_by_user_and_announcement(db_session, create_user):
    user = await create_user(email="rr_user@example.com", password="x")
    game = Game(name="RRGame", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    ann = Announcement(
        title="Ann1",
        content="c",
        game_id=game.id,
        organizer_id=user.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr_in = RegistrationRequestCreate(announcement_id=ann.id)
    created = await registration_request_crud.create(
        session=db_session, registration_request_in=rr_in, user=user
    )

    user_list, user_total = await registration_request_crud.get_all_by_user_id(
        session=db_session, user_id=user.id
    )
    assert any(r.id == created.id for r in user_list)
    assert user_total >= 1

    ann_list, ann_total = await registration_request_crud.get_all_by_announcement_id(
        session=db_session, announcement_id=ann.id
    )
    assert any(r.id == created.id for r in ann_list)
    assert ann_total >= 1


@pytest.mark.asyncio
async def test_get_by_user_and_announcement(db_session, create_user):
    user = await create_user(email="rr_user2@example.com", password="x")
    game = Game(name="RRGame2", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    ann = Announcement(
        title="Ann2",
        content="c",
        game_id=game.id,
        organizer_id=user.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr_in = RegistrationRequestCreate(announcement_id=ann.id)
    created = await registration_request_crud.create(
        session=db_session, registration_request_in=rr_in, user=user
    )

    found = await registration_request_crud.get_by_user_and_announcement(
        session=db_session, user_id=user.id, announcement_id=ann.id
    )
    assert found is not None and found.id == created.id


@pytest.mark.asyncio
async def test_get_by_id_loads_relations(db_session, create_user):
    user = await create_user(email="rr_user3@example.com", password="x")
    game = Game(name="RRGame3", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    ann = Announcement(
        title="Ann3",
        content="c",
        game_id=game.id,
        organizer_id=user.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr_in = RegistrationRequestCreate(announcement_id=ann.id)
    created = await registration_request_crud.create(
        session=db_session, registration_request_in=rr_in, user=user
    )

    got = await registration_request_crud.get_by_id(
        session=db_session, registration_request_id=created.id
    )
    assert got.id == created.id


@pytest.mark.asyncio
async def test_approve_registration_request(db_session, create_user):
    owner = await create_user(email="owner@example.com", password="x")
    actor = await create_user(email="actor@example.com", password="x")

    game = Game(name="RRGame3", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    ann = Announcement(
        title="Ann3",
        content="c",
        game_id=game.id,
        organizer_id=owner.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr_in = RegistrationRequestCreate(announcement_id=ann.id)
    created = await registration_request_crud.create(
        session=db_session, registration_request_in=rr_in, user=actor
    )

    rr = await registration_request_crud.get_by_id(
        session=db_session, registration_request_id=created.id
    )

    with patch("api.v1.crud.registration_request.authorize_action"):
        approved = await registration_request_crud.approve(
            session=db_session, registration_request=rr, user=owner
        )
    assert approved.status == RegistrationStatus.APPROVED

    res = await db_session.execute(
        select(RegistrationRequest).where(RegistrationRequest.id == approved.id)
    )
    rr_row = res.scalar_one_or_none()
    assert rr_row.status == RegistrationStatus.APPROVED


@pytest.mark.asyncio
async def test_reject_registration_request(db_session, create_user):
    owner = await create_user(email="owner2@example.com", password="x")
    actor = await create_user(email="actor2@example.com", password="x")

    game = Game(name="RRGame4", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    ann = Announcement(
        title="Ann4",
        content="c",
        game_id=game.id,
        organizer_id=owner.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr_in = RegistrationRequestCreate(announcement_id=ann.id)
    rr = await registration_request_crud.create(
        session=db_session, registration_request_in=rr_in, user=actor
    )
    rr_loaded = await registration_request_crud.get_by_id(
        session=db_session, registration_request_id=rr.id
    )
    with patch("api.v1.crud.registration_request.authorize_action"):
        rejected = await registration_request_crud.reject(
            session=db_session, registration_request=rr_loaded, user=owner
        )
    assert rejected.status == RegistrationStatus.REJECTED


@pytest.mark.asyncio
async def test_cancel_registration_request(db_session, create_user):
    owner = await create_user(email="owner3@example.com", password="x")
    actor = await create_user(email="actor3@example.com", password="x")

    game = Game(name="RRGame5", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    ann = Announcement(
        title="Ann5",
        content="c",
        game_id=game.id,
        organizer_id=owner.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
    )
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr_in = RegistrationRequestCreate(announcement_id=ann.id)
    rr3 = await registration_request_crud.create(
        session=db_session, registration_request_in=rr_in, user=actor
    )
    rr3_loaded = await registration_request_crud.get_by_id(
        session=db_session, registration_request_id=rr3.id
    )
    with patch("api.v1.crud.registration_request.authorize_action"):
        cancelled = await registration_request_crud.cancel(
            session=db_session, registration_request=rr3_loaded, user=actor
        )
    assert cancelled.status == RegistrationStatus.CANCELLED
