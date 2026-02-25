import pytest
from datetime import datetime

from pydantic import ValidationError
from domains.announcements.schemas import (
    AnnouncementCreate,
    AnnouncementUpdate,
    AnnouncementResponse,
    AnnouncementFilter,
    AnnouncementParticipantBase,
    AnnouncementParticipantUpdate,
    AnnouncementParticipantResponse,
)
from enums import AnnouncementFormat, SeedMethod


def test_announcement_create_and_update_models():
    now = datetime.now()
    create = AnnouncementCreate(
        title="T",
        content="C",
        game_id=1,
        start_at=now,
        registration_start_at=now,
        registration_end_at=now,
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
    )
    assert create.title == "T"
    upd = AnnouncementUpdate(title="New", max_participants=20)
    assert upd.title == "New"


def test_announcement_response_includes_permissions_and_timestamps():
    now = datetime.now()
    resp = AnnouncementResponse(
        id=1,
        title="X",
        content=None,
        game_id=2,
        created_at=now,
        updated_at=now,
        organizer_id=5,
        start_at=now,
        registration_start_at=now,
        registration_end_at=now,
        is_registration_open=True,
        max_participants=10,
        status="pre_registration",
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    assert resp.id == 1
    assert resp.permissions == {}
    assert resp.created_at == now


def test_announcement_response_participants_count_empty():
    now = datetime.now()
    resp = AnnouncementResponse(
        id=1,
        title="X",
        content=None,
        game_id=2,
        created_at=now,
        updated_at=now,
        organizer_id=5,
        start_at=now,
        registration_start_at=now,
        registration_end_at=now,
        max_participants=10,
        status="pre_registration",
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
        participants=[],
    )
    assert resp.participants_count == 0


def test_announcement_response_participants_count_with_participants():
    now = datetime.now()
    resp = AnnouncementResponse(
        id=1,
        title="X",
        content=None,
        game_id=2,
        created_at=now,
        updated_at=now,
        organizer_id=5,
        start_at=now,
        registration_start_at=now,
        registration_end_at=now,
        max_participants=10,
        status="pre_registration",
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
        participants=[
            {
                "id": i,
                "announcement_id": 1,
                "user_id": i,
                "qualification_score": None,
                "qualification_rank": None,
                "seed": None,
                "is_qualified": False,
                "created_at": now,
                "updated_at": now,
            }
            for i in [1, 2, 3]
        ],
    )
    assert resp.participants_count == 3


def test_announcement_response_participants_excluded_from_json():
    now = datetime.now()
    resp = AnnouncementResponse(
        id=1,
        title="X",
        content=None,
        game_id=2,
        created_at=now,
        updated_at=now,
        organizer_id=5,
        start_at=now,
        registration_start_at=now,
        registration_end_at=now,
        max_participants=10,
        status="pre_registration",
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
        participants=[
            {
                "id": i,
                "announcement_id": 1,
                "user_id": i,
                "qualification_score": None,
                "qualification_rank": None,
                "seed": None,
                "is_qualified": False,
                "created_at": now,
                "updated_at": now,
            }
            for i in [1, 2]
        ],
    )
    data = resp.model_dump()
    assert "participants" not in data
    assert "participants_count" in data
    assert data["participants_count"] == 2


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
    assert response.qualification_score == 95
    assert response.user is not None
    assert response.user.email == "test@example.com"


def test_announcement_filter_all_fields_none():
    filter = AnnouncementFilter()
    assert filter.values() == {}


def test_announcement_filter_with_game_id():
    filter = AnnouncementFilter(game_id=123)
    assert filter.values() == {"game_id": 123}


def test_announcement_filter_with_status():
    filter = AnnouncementFilter(status="registration_open")
    assert filter.values() == {"status": "registration_open"}


def test_announcement_filter_excludes_none_values():
    filter = AnnouncementFilter(game_id=789, status=None)
    assert filter.values() == {"game_id": 789}
    assert "status" not in filter.values()


def test_announcement_filter_search_query_trims_whitespace():
    filter = AnnouncementFilter(q="  test query  ")
    assert filter.q == "test query"


def test_announcement_filter_search_query_empty_string_becomes_none():
    filter = AnnouncementFilter(q="   ")
    assert filter.q is None
    assert "q" not in filter.values()


def test_announcement_filter_with_all_fields_including_q():
    filter = AnnouncementFilter(game_id=1, status="live", q="tournament")
    assert filter.values() == {"game_id": 1, "status": "live", "q": "tournament"}


def test_announcement_filter_search_query_max_length_exceeded():
    """Test that search query exceeding 100 characters is rejected."""
    invalid_query = "a" * 101
    with pytest.raises(ValidationError) as exc_info:
        AnnouncementFilter(q=invalid_query)

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("q",)
    assert "String should have at most 100 characters" in errors[0]["msg"]
