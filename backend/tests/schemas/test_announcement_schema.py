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
    )
    assert create.title == "T"
    upd = AnnouncementUpdate(title="New")
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
    )
    assert resp.id == 1
    assert resp.permissions == {}
    assert resp.created_at == now
