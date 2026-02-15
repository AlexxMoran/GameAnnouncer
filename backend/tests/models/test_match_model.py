import pytest
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.match import Match
from models.announcement import Announcement
from exceptions import ValidationException
from enums import MatchStatus


def test_match_tablename_and_columns():
    """Test Match table name and column presence."""
    assert Match.__tablename__ == "matches"

    cols = Match.__table__.columns
    assert "id" in cols
    assert "announcement_id" in cols
    assert "round_number" in cols
    assert "match_number" in cols
    assert "participant1_id" in cols
    assert "participant2_id" in cols
    assert "participant1_score" in cols
    assert "participant2_score" in cols
    assert "winner_id" in cols
    assert "next_match_winner_id" in cols
    assert "status" in cols
    assert "is_bye" in cols
    assert "is_third_place" in cols
    assert "completed_at" in cols


def test_match_primary_and_foreign_keys():
    """Test Match primary and foreign key constraints."""
    id_col = Match.__table__.c["id"]
    announcement_col = Match.__table__.c["announcement_id"]
    participant1_col = Match.__table__.c["participant1_id"]
    participant2_col = Match.__table__.c["participant2_id"]
    winner_col = Match.__table__.c["winner_id"]
    next_match_col = Match.__table__.c["next_match_winner_id"]

    assert id_col.primary_key is True
    assert announcement_col.primary_key is False

    assert any(
        fk.column.table.name == "announcements" for fk in announcement_col.foreign_keys
    )
    assert any(
        fk.column.table.name == "announcement_participants"
        for fk in participant1_col.foreign_keys
    )
    assert any(
        fk.column.table.name == "announcement_participants"
        for fk in participant2_col.foreign_keys
    )
    assert any(
        fk.column.table.name == "announcement_participants"
        for fk in winner_col.foreign_keys
    )
    assert any(fk.column.table.name == "matches" for fk in next_match_col.foreign_keys)


def test_match_relationships():
    """Test Match relationships exist."""
    rels = {r.key for r in Match.__mapper__.relationships}
    assert "announcement" in rels
    assert "participant1" in rels
    assert "participant2" in rels
    assert "winner" in rels
    assert "next_match_winner" in rels


def test_match_indexes():
    """Test Match indexes are defined."""
    indexes = {idx.name for idx in Match.__table__.indexes}
    assert "idx_match_round" in indexes


def test_match_constraints():
    """Test Match constraints are defined."""
    constraints = {c.name for c in Match.__table__.constraints if hasattr(c, "name")}
    assert "uq_match_position" in constraints
    assert "ck_matches_winner_must_be_participant" in constraints


def test_validate_negative_participant1_score():
    """Test that participant1_score cannot be negative."""
    match = Match(announcement_id=1, round_number=1, match_number=1)

    with pytest.raises(ValidationException) as exc_info:
        match.participant1_score = -1
    assert "participant1_score cannot be negative" in str(exc_info.value)

    match.participant1_score = 0
    assert match.participant1_score == 0

    match.participant1_score = 10
    assert match.participant1_score == 10

    match.participant1_score = None
    assert match.participant1_score is None


def test_validate_negative_participant2_score():
    """Test that participant2_score cannot be negative."""
    match = Match(announcement_id=1, round_number=1, match_number=1)

    with pytest.raises(ValidationException) as exc_info:
        match.participant2_score = -5
    assert "participant2_score cannot be negative" in str(exc_info.value)

    match.participant2_score = 0
    assert match.participant2_score == 0

    match.participant2_score = 15
    assert match.participant2_score == 15

    match.participant2_score = None
    assert match.participant2_score is None


def test_validate_round_number_must_be_positive():
    """Test that round_number must be positive."""
    with pytest.raises(ValidationException) as exc_info:
        Match(announcement_id=1, round_number=0, match_number=1)
    assert "round_number must be positive" in str(exc_info.value)

    with pytest.raises(ValidationException) as exc_info:
        Match(announcement_id=1, round_number=-1, match_number=1)
    assert "round_number must be positive" in str(exc_info.value)

    match = Match(announcement_id=1, round_number=1, match_number=1)
    assert match.round_number == 1


def test_validate_match_number_must_be_positive():
    """Test that match_number must be positive."""
    with pytest.raises(ValidationException) as exc_info:
        Match(announcement_id=1, round_number=1, match_number=0)
    assert "match_number must be positive" in str(exc_info.value)

    with pytest.raises(ValidationException) as exc_info:
        Match(announcement_id=1, round_number=1, match_number=-1)
    assert "match_number must be positive" in str(exc_info.value)

    match = Match(announcement_id=1, round_number=1, match_number=1)
    assert match.match_number == 1


@pytest.mark.asyncio
async def test_create_valid_match(
    create_user, create_announcement, create_participant, create_match
):
    """Test creating a valid match with all fields."""
    user = await create_user(email="match_user@example.com")
    announcement = await create_announcement(organizer_id=user.id)
    participant1 = await create_participant(
        announcement_id=announcement.id, user_id=user.id, seed=1
    )

    match = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        participant1_id=participant1.id,
        participant1_score=10,
    )

    assert match.id is not None
    assert match.announcement_id == announcement.id
    assert match.round_number == 1
    assert match.match_number == 1
    assert match.participant1_id == participant1.id
    assert match.participant1_score == 10
    assert match.status == MatchStatus.PENDING


@pytest.mark.asyncio
async def test_match_cascade_delete_on_announcement(
    db_session, create_user, create_announcement, create_match
):
    """Test that deleting announcement cascades to matches."""
    user = await create_user(email="cascade@example.com")
    announcement = await create_announcement(organizer_id=user.id)

    match = await create_match(
        announcement_id=announcement.id, round_number=1, match_number=1
    )
    match_id = match.id

    await db_session.delete(announcement)
    await db_session.commit()

    result = await db_session.execute(select(Match).where(Match.id == match_id))
    deleted_match = result.scalar_one_or_none()
    assert deleted_match is None


@pytest.mark.asyncio
async def test_match_set_null_on_participant_delete(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """Test that deleting participant sets FK to NULL."""
    user = await create_user(email="setnull@example.com")
    announcement = await create_announcement(organizer_id=user.id)

    participant1 = await create_participant(
        announcement_id=announcement.id, user_id=user.id, seed=1
    )

    match = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        participant1_id=participant1.id,
    )
    match_id = match.id

    await db_session.delete(participant1)
    await db_session.commit()

    # Expire session to clear cache and fetch fresh data from DB
    db_session.expire_all()

    result = await db_session.execute(select(Match).where(Match.id == match_id))
    updated_match = result.scalar_one_or_none()
    assert updated_match is not None
    assert updated_match.participant1_id is None


@pytest.mark.asyncio
async def test_match_relationships_loaded(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """Test that match relationships can be loaded."""
    user = await create_user(email="relationships@example.com")
    announcement = await create_announcement(organizer_id=user.id)

    participant1 = await create_participant(
        announcement_id=announcement.id, user_id=user.id, seed=1
    )

    next_match = await create_match(
        announcement_id=announcement.id, round_number=2, match_number=1
    )

    match = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        participant1_id=participant1.id,
        next_match_winner_id=next_match.id,
    )

    result = await db_session.execute(
        select(Match)
        .where(Match.id == match.id)
        .options(
            selectinload(Match.announcement),
            selectinload(Match.participant1),
            selectinload(Match.next_match_winner),
        )
    )
    loaded_match = result.scalar_one()

    assert loaded_match.announcement.id == announcement.id
    assert loaded_match.participant1.id == participant1.id
    assert loaded_match.next_match_winner.id == next_match.id


@pytest.mark.asyncio
async def test_announcement_matches_relationship(
    db_session, create_user, create_announcement, create_match
):
    """Test that announcement.matches relationship works."""
    user = await create_user(email="ann_matches@example.com")
    announcement = await create_announcement(organizer_id=user.id)

    await create_match(announcement_id=announcement.id, round_number=1, match_number=1)
    await create_match(announcement_id=announcement.id, round_number=1, match_number=2)

    result = await db_session.execute(
        select(Announcement)
        .where(Announcement.id == announcement.id)
        .options(selectinload(Announcement.matches))
    )
    loaded_announcement = result.scalar_one()
    matches = loaded_announcement.matches

    assert len(matches) == 2
    assert any(m.match_number == 1 for m in matches)
    assert any(m.match_number == 2 for m in matches)


@pytest.mark.asyncio
async def test_match_with_completed_at(
    create_user, create_announcement, create_participant, create_match
):
    """Test match with completed_at timestamp."""
    user = await create_user(email="completed@example.com")
    announcement = await create_announcement(organizer_id=user.id)
    participant1 = await create_participant(
        announcement_id=announcement.id, user_id=user.id, seed=1
    )

    completed_time = datetime.now()
    match = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        participant1_id=participant1.id,
        winner_id=participant1.id,
        status=MatchStatus.COMPLETED,
        completed_at=completed_time,
    )

    assert match.completed_at is not None
    assert match.status == MatchStatus.COMPLETED
    assert match.winner_id == participant1.id


@pytest.mark.asyncio
async def test_match_with_bye(create_user, create_announcement, create_match):
    """Test BYE match creation."""
    user = await create_user(email="bye@example.com")
    announcement = await create_announcement(organizer_id=user.id)

    match = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        is_bye=True,
        status=MatchStatus.BYE,
    )

    assert match.is_bye is True
    assert match.status == MatchStatus.BYE
    assert match.participant1_id is None
    assert match.participant2_id is None


@pytest.mark.asyncio
async def test_match_third_place(create_user, create_announcement, create_match):
    """Test third place match creation."""
    user = await create_user(email="third@example.com")
    announcement = await create_announcement(organizer_id=user.id)

    match = await create_match(
        announcement_id=announcement.id,
        round_number=3,
        match_number=1,
        is_third_place=True,
    )

    assert match.is_third_place is True
    assert match.round_number == 3
    assert match.status == MatchStatus.PENDING


def test_match_repr():
    """Test __repr__ method."""
    match = Match(
        announcement_id=5,
        round_number=2,
        match_number=3,
        status=MatchStatus.IN_PROGRESS,
    )
    match.id = 42

    repr_str = repr(match)
    assert "Match" in repr_str
    assert "id=42" in repr_str
    assert "announcement_id=5" in repr_str
    assert "round=2" in repr_str
    assert "match=3" in repr_str
    assert "status=IN_PROGRESS" in repr_str
