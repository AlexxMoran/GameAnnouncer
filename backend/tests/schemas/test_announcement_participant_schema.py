from datetime import datetime

from schemas.announcement_participant import (
    AnnouncementParticipantBase,
    AnnouncementParticipantUpdate,
    AnnouncementParticipantResponse,
)


def test_announcement_participant_base_defaults():
    """Test AnnouncementParticipantBase with default values."""
    base = AnnouncementParticipantBase()
    assert base.qualification_score is None
    assert base.qualification_rank is None
    assert base.seed is None
    assert base.is_qualified is False


def test_announcement_participant_base_with_values():
    """Test AnnouncementParticipantBase with custom values."""
    base = AnnouncementParticipantBase(
        qualification_score=100,
        qualification_rank=5,
        seed=3,
        is_qualified=True,
    )
    assert base.qualification_score == 100
    assert base.qualification_rank == 5
    assert base.seed == 3
    assert base.is_qualified is True


def test_announcement_participant_update_all_optional():
    """Test AnnouncementParticipantUpdate with optional fields."""
    update = AnnouncementParticipantUpdate()
    assert update.qualification_score is None
    assert update.qualification_rank is None
    assert update.seed is None
    assert update.is_qualified is None


def test_announcement_participant_update_partial():
    """Test AnnouncementParticipantUpdate with partial update."""
    update = AnnouncementParticipantUpdate(
        qualification_score=85,
        is_qualified=True,
    )
    assert update.qualification_score == 85
    assert update.qualification_rank is None
    assert update.seed is None
    assert update.is_qualified is True


def test_announcement_participant_response_required_fields():
    """Test AnnouncementParticipantResponse with required fields."""
    now = datetime.now()
    response = AnnouncementParticipantResponse(
        id=1,
        announcement_id=10,
        user_id=5,
        created_at=now,
        updated_at=now,
        qualification_score=None,
        qualification_rank=None,
        seed=None,
        is_qualified=False,
    )
    assert response.id == 1
    assert response.announcement_id == 10
    assert response.user_id == 5
    assert response.created_at == now
    assert response.updated_at == now
    assert response.qualification_score is None
    assert response.qualification_rank is None
    assert response.seed is None
    assert response.is_qualified is False
    assert response.user is None


def test_announcement_participant_response_with_all_fields():
    """Test AnnouncementParticipantResponse with all fields populated."""
    now = datetime.now()
    user_data = {
        "id": 5,
        "email": "test@example.com",
        "is_active": True,
        "is_superuser": False,
        "is_verified": True,
        "first_name": "John",
        "last_name": "Doe",
        "nickname": "johndoe",
    }
    response = AnnouncementParticipantResponse(
        id=1,
        announcement_id=10,
        user_id=5,
        created_at=now,
        updated_at=now,
        qualification_score=95,
        qualification_rank=2,
        seed=1,
        is_qualified=True,
        user=user_data,
    )
    assert response.id == 1
    assert response.announcement_id == 10
    assert response.user_id == 5
    assert response.qualification_score == 95
    assert response.qualification_rank == 2
    assert response.seed == 1
    assert response.is_qualified is True
    assert response.user is not None
    assert response.user.id == 5
    assert response.user.email == "test@example.com"


def test_announcement_participant_response_model_dump():
    """Test AnnouncementParticipantResponse serialization."""
    now = datetime.now()
    response = AnnouncementParticipantResponse(
        id=1,
        announcement_id=10,
        user_id=5,
        created_at=now,
        updated_at=now,
        qualification_score=80,
        qualification_rank=3,
        seed=2,
        is_qualified=True,
    )
    data = response.model_dump()
    assert data["id"] == 1
    assert data["announcement_id"] == 10
    assert data["user_id"] == 5
    assert data["qualification_score"] == 80
    assert data["qualification_rank"] == 3
    assert data["seed"] == 2
    assert data["is_qualified"] is True
    assert "created_at" in data
    assert "updated_at" in data
