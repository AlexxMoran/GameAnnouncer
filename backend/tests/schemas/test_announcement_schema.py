from datetime import datetime

from schemas.announcement import (
    AnnouncementCreate,
    AnnouncementUpdate,
    AnnouncementResponse,
)


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
