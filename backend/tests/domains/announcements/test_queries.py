import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy import insert

from domains.announcements.model import Announcement
from domains.announcements.queries import AnnouncementQueries
from domains.games.model import Game
from domains.participants.model import AnnouncementParticipant
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
async def test_find_all_by_organizer_id(db_session, create_user):
    user = await create_user(email="creator3@example.com", password="x")
    game = Game(name="G-org", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, "Org A")
    db_session.add(ann)
    await db_session.commit()

    queries = AnnouncementQueries(db_session)
    org_results, org_total = await queries.find_all_by_organizer_id(user.id)

    assert any(result.organizer_id == user.id for result in org_results)
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

    queries = AnnouncementQueries(db_session)
    part_results, part_total = await queries.find_all_by_participant_id(user.id)

    assert any(result.id == ann.id for result in part_results)
    assert part_total >= 1


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

    queries = AnnouncementQueries(db_session)
    got = await queries.find_by_id(ann.id)

    assert got is not None
    assert got.id == ann.id
