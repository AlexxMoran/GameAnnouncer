from datetime import datetime, timezone

from schemas.announcement import (
    AnnouncementCreate,
    AnnouncementUpdate,
    AnnouncementResponse,
)


def test_announcement_create_and_update_models():
    create = AnnouncementCreate(title="T", content="C", game_id=1)
    assert create.title == "T"
    upd = AnnouncementUpdate(title="New")
    assert upd.title == "New"


def test_announcement_response_includes_permissions_and_timestamps():
    now = datetime.now(timezone.utc)
    resp = AnnouncementResponse(
        id=1,
        title="X",
        content=None,
        game_id=2,
        created_at=now,
        updated_at=now,
        organizer_id=5,
    )
    assert resp.id == 1
    assert resp.permissions == {}
    assert resp.created_at == now
