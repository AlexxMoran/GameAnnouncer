import pytest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone

from sqlalchemy import insert, select

from api.v1.crud.announcement import announcement_crud
from models.announcement import Announcement
from models.game import Game
from schemas.announcement import (
    AnnouncementCreate,
    AnnouncementUpdate,
    AnnouncementAction,
)
from enums import AnnouncementStatus, AnnouncementFormat
from exceptions import ValidationException


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
        format=AnnouncementFormat.SINGLE_ELIMINATION,
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
        format=AnnouncementFormat.SINGLE_ELIMINATION,
    )
    a2 = AnnouncementCreate(
        title="L2",
        content="c2",
        game_id=game.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
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
        format=AnnouncementFormat.SINGLE_ELIMINATION,
    )
    created = await announcement_crud.create(
        session=db_session, announcement_in=a_in, user=user
    )

    org_results, org_total = await announcement_crud.get_all_by_organizer_id(
        session=db_session, organizer_id=user.id
    )
    assert any(r.organizer_id == user.id for r in org_results)
    assert org_total >= 1

    from models.announcement_participant import AnnouncementParticipant

    await db_session.execute(
        insert(AnnouncementParticipant).values(
            announcement_id=created.id, user_id=user.id
        )
    )
    await db_session.commit()

    part_results, part_total = await announcement_crud.get_all_by_participant_id(
        session=db_session, user_id=user.id
    )
    assert any(r.id == created.id for r in part_results)
    assert part_total >= 1

    (
        participants,
        participants_total,
    ) = await announcement_crud.get_participants_by_announcement_id(
        session=db_session, announcement_id=created.id
    )
    assert any(p.user_id == user.id for p in participants)
    assert participants_total >= 1


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
        format=AnnouncementFormat.SINGLE_ELIMINATION,
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
        format=AnnouncementFormat.SINGLE_ELIMINATION,
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


@pytest.mark.asyncio
async def test_update_status_finish_success(db_session, create_user):
    user = await create_user(email="creator6@example.com", password="x")
    game = Game(name="G-finish", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    a_in = AnnouncementCreate(
        title="ToFinish",
        content="c",
        game_id=game.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
    )
    created = await announcement_crud.create(
        session=db_session, announcement_in=a_in, user=user
    )

    # Manually set status to LIVE
    created.status = AnnouncementStatus.LIVE
    await db_session.commit()
    await db_session.refresh(created)

    with patch("api.v1.crud.announcement.authorize_action"):
        updated = await announcement_crud.update_status(
            session=db_session,
            announcement=created,
            action=AnnouncementAction.FINISH,
            user=user,
        )

    assert updated.status == AnnouncementStatus.FINISHED
    assert updated.end_at is not None


@pytest.mark.asyncio
async def test_update_status_finish_wrong_status(db_session, create_user):
    user = await create_user(email="creator7@example.com", password="x")
    game = Game(name="G-finish-fail", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    a_in = AnnouncementCreate(
        title="WrongStatus",
        content="c",
        game_id=game.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
    )
    created = await announcement_crud.create(
        session=db_session, announcement_in=a_in, user=user
    )

    # Status should be REGISTRATION_OPEN, not LIVE
    with patch("api.v1.crud.announcement.authorize_action"):
        with pytest.raises(ValidationException) as exc_info:
            await announcement_crud.update_status(
                session=db_session,
                announcement=created,
                action=AnnouncementAction.FINISH,
                user=user,
            )
    assert "Can only finish announcement when it is 'live'" in str(exc_info.value)


@pytest.mark.asyncio
async def test_update_status_cancel_success(db_session, create_user):
    user = await create_user(email="creator8@example.com", password="x")
    game = Game(name="G-cancel", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    a_in = AnnouncementCreate(
        title="ToCancel",
        content="c",
        game_id=game.id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
    )
    created = await announcement_crud.create(
        session=db_session, announcement_in=a_in, user=user
    )

    with patch("api.v1.crud.announcement.authorize_action"):
        updated = await announcement_crud.update_status(
            session=db_session,
            announcement=created,
            action=AnnouncementAction.CANCEL,
            user=user,
        )

    assert updated.status == AnnouncementStatus.CANCELLED
