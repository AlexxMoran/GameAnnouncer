import pytest
from models.announcement_participant import AnnouncementParticipant
from exceptions import ValidationException


def test_tablename_and_columns():
    assert AnnouncementParticipant.__tablename__ == "announcement_participants"

    cols = AnnouncementParticipant.__table__.columns
    assert "id" in cols
    assert "announcement_id" in cols
    assert "user_id" in cols
    assert "qualification_score" in cols
    assert "qualification_rank" in cols
    assert "seed" in cols
    assert "is_qualified" in cols


def test_columns_primary_and_foreign_keys():
    id_col = AnnouncementParticipant.__table__.c["id"]
    announcement_col = AnnouncementParticipant.__table__.c["announcement_id"]
    user_col = AnnouncementParticipant.__table__.c["user_id"]

    assert id_col.primary_key is True
    assert announcement_col.primary_key is False
    assert user_col.primary_key is False
    assert any(
        fk.column.table.name == "announcements" for fk in announcement_col.foreign_keys
    )
    assert any(fk.column.table.name == "users" for fk in user_col.foreign_keys)


def test_validate_positive_seed():
    """Test that seed must be positive."""
    participant = AnnouncementParticipant(announcement_id=1, user_id=1)

    with pytest.raises(ValidationException) as exc_info:
        participant.seed = 0
    assert "seed must be a positive number" in str(exc_info.value)

    with pytest.raises(ValidationException) as exc_info:
        participant.seed = -5
    assert "seed must be a positive number" in str(exc_info.value)

    participant.seed = 1
    assert participant.seed == 1

    participant.seed = None
    assert participant.seed is None


def test_validate_positive_qualification_rank():
    """Test that qualification_rank must be positive."""
    participant = AnnouncementParticipant(announcement_id=1, user_id=1)

    with pytest.raises(ValidationException) as exc_info:
        participant.qualification_rank = 0
    assert "qualification_rank must be a positive number" in str(exc_info.value)

    with pytest.raises(ValidationException) as exc_info:
        participant.qualification_rank = -10
    assert "qualification_rank must be a positive number" in str(exc_info.value)

    participant.qualification_rank = 5
    assert participant.qualification_rank == 5

    participant.qualification_rank = None
    assert participant.qualification_rank is None


def test_validate_positive_qualification_score():
    """Test that qualification_score must be positive."""
    participant = AnnouncementParticipant(announcement_id=1, user_id=1)

    with pytest.raises(ValidationException) as exc_info:
        participant.qualification_score = 0
    assert "qualification_score must be a positive number" in str(exc_info.value)

    with pytest.raises(ValidationException) as exc_info:
        participant.qualification_score = -100
    assert "qualification_score must be a positive number" in str(exc_info.value)

    participant.qualification_score = 95
    assert participant.qualification_score == 95

    participant.qualification_score = None
    assert participant.qualification_score is None


def test_repr():
    """Test __repr__ method."""
    participant = AnnouncementParticipant(
        announcement_id=10,
        user_id=5,
        seed=3,
        qualification_rank=2,
        is_qualified=True,
    )
    participant.id = 1

    repr_str = repr(participant)
    assert "AnnouncementParticipant" in repr_str
    assert "id=1" in repr_str
    assert "announcement_id=10" in repr_str
    assert "user_id=5" in repr_str
    assert "seed=3" in repr_str
    assert "rank=2" in repr_str
    assert "qualified=True" in repr_str
