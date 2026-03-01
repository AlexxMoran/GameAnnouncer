import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy import insert, select

from domains.announcements.model import Announcement
from domains.participants.model import AnnouncementParticipant
from domains.announcements.repository import AnnouncementRepository
from domains.participants.repository import ParticipantRepository
from domains.games.model import Game
from enums import AnnouncementFormat, SeedMethod


def _make_announcement(
    game_id: int, organizer_id: int, title: str = "T"
) -> Announcement:
    now = datetime.now(timezone.utc)
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
async def test_save_creates_announcement(db_session, create_user):
    user = await create_user(email="creator1@example.com", password="x")
    game = Game(name="G-create", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, "Create A")
    repo = AnnouncementRepository(db_session)
    created = await repo.save(ann)
    await db_session.commit()

    assert created.id is not None
    assert created.organizer_id == user.id


@pytest.mark.asyncio
async def test_find_all_by_organizer_id(db_session, create_user):
    user = await create_user(email="creator3@example.com", password="x")
    game = Game(name="G-org", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, "Org A")
    db_session.add(ann)
    await db_session.commit()

    repo = AnnouncementRepository(db_session)
    org_results, org_total = await repo.find_all_by_organizer_id(user.id)

    assert any(r.organizer_id == user.id for r in org_results)
    assert org_total >= 1


@pytest.mark.asyncio
async def test_find_all_by_participant_id(db_session, create_user):
    user = await create_user(email="creator3b@example.com", password="x")
    game = Game(name="G-part", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, "Part A")
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    await db_session.execute(
        insert(AnnouncementParticipant).values(announcement_id=ann.id, user_id=user.id)
    )
    await db_session.commit()

    repo = AnnouncementRepository(db_session)
    part_results, part_total = await repo.find_all_by_participant_id(user.id)

    assert any(r.id == ann.id for r in part_results)
    assert part_total >= 1


@pytest.mark.asyncio
async def test_find_participants_by_announcement_id(db_session, create_user):
    user = await create_user(email="creator3c@example.com", password="x")
    game = Game(name="G-plist", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, "PList A")
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    await db_session.execute(
        insert(AnnouncementParticipant).values(announcement_id=ann.id, user_id=user.id)
    )
    await db_session.commit()

    repo = ParticipantRepository(db_session)
    participants, total = await repo.find_all_by_announcement_id(ann.id)

    assert any(p.user_id == user.id for p in participants)
    assert total >= 1


@pytest.mark.asyncio
async def test_find_by_id_returns_announcement(db_session, create_user):
    user = await create_user(email="creator4@example.com", password="x")
    game = Game(name="G-get", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, "G1")
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    repo = AnnouncementRepository(db_session)
    got = await repo.find_by_id(ann.id)

    assert got is not None
    assert got.id == ann.id


@pytest.mark.asyncio
async def test_save_updates_announcement(db_session, create_user):
    user = await create_user(email="creator4b@example.com", password="x")
    game = Game(name="G-upd", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, "G1")
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    ann.title = "Updated Title"
    repo = AnnouncementRepository(db_session)
    updated = await repo.save(ann)
    await db_session.commit()

    assert updated.title == "Updated Title"


@pytest.mark.asyncio
async def test_delete_announcement(db_session, create_user):
    user = await create_user(email="creator5@example.com", password="x")
    game = Game(name="G-del", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, "ToDelete")
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    repo = AnnouncementRepository(db_session)
    await repo.delete(ann)
    await db_session.commit()

    res = await db_session.execute(
        select(Announcement).where(Announcement.id == ann.id)
    )
    assert res.scalar_one_or_none() is None
