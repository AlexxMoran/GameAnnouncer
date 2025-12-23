import pytest
from types import SimpleNamespace


@pytest.mark.asyncio
async def test_get_announcements_paginated(
    async_client, announcement_factory, monkeypatch
):
    game_id = 123
    a1 = announcement_factory.build(organizer_id=1)
    a2 = announcement_factory.build(organizer_id=2)
    announcements = [SimpleNamespace(**a1), SimpleNamespace(**a2)]

    async def _fake_get_all_by_game_id(session, game_id, skip=0, limit=10):
        assert game_id == game_id
        return announcements

    async def _fake_get_all_count_by_game_id(session, game_id):
        assert game_id == game_id
        return 2

    monkeypatch.setattr(
        "api.v1.announcements.announcement_crud.get_all_by_game_id",
        _fake_get_all_by_game_id,
    )
    monkeypatch.setattr(
        "api.v1.announcements.announcement_crud.get_all_count_by_game_id",
        _fake_get_all_count_by_game_id,
    )

    monkeypatch.setattr(
        "api.v1.announcements.get_batch_permissions", lambda user, anns: None
    )

    r = await async_client.get(f"/api/v1/games/{game_id}/announcements?skip=0&limit=10")
    assert r.status_code == 200
    body = r.json()
    assert body["data"][0]["id"] == a1["id"]
    assert body["data"][1]["id"] == a2["id"]
    assert body["skip"] == 0
    assert body["limit"] == 10
    assert body["total"] == 2


@pytest.mark.asyncio
async def test_get_announcement_and_permissions(
    async_client, announcement_factory, monkeypatch
):
    a = announcement_factory.build()
    ann_obj = SimpleNamespace(**a)

    async def _fake_get_by_id(session, announcement_id, user=None, action=None):
        return ann_obj

    monkeypatch.setattr(
        "api.v1.announcements.announcement_crud.get_by_id",
        _fake_get_by_id,
    )

    monkeypatch.setattr(
        "api.v1.announcements.get_permissions", lambda user, ann: {"edit": True}
    )

    r = await async_client.get(f"/api/v1/games/1/announcements/{a['id']}")
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["id"] == a["id"]
    assert data["organizer_id"] == a["organizer_id"]
    assert data["permissions"]["edit"] is True


@pytest.mark.asyncio
async def test_get_announcement_participants(
    async_client, announcement_factory, monkeypatch
):
    a = announcement_factory.build()

    async def _fake_get_by_id(session, announcement_id):
        return SimpleNamespace(**a)

    participants = [{"id": 5, "email": "p@example.com"}]

    async def _fake_get_participants(session, announcement):
        assert announcement.id == a["id"]
        return participants

    monkeypatch.setattr(
        "api.v1.announcements.announcement_crud.get_by_id",
        _fake_get_by_id,
    )
    monkeypatch.setattr(
        "api.v1.announcements.announcement_crud.get_participants_by_announcement_id",
        _fake_get_participants,
    )

    r = await async_client.get(f"/api/v1/games/1/announcements/{a['id']}/participants")
    assert r.status_code == 200
    assert r.json()["data"][0]["email"] == "p@example.com"


@pytest.mark.asyncio
async def test_get_announcement_registration_requests(
    async_client, announcement_factory, registration_request_factory, monkeypatch
):
    a = announcement_factory.build()

    async def _fake_get_by_id(session, announcement_id):
        return SimpleNamespace(**a)

    fake_rr = [registration_request_factory.build(announcement_id=a["id"])]

    async def _fake_get_rr(session, announcement_id):
        assert announcement_id == a["id"]
        return fake_rr

    monkeypatch.setattr(
        "api.v1.announcements.announcement_crud.get_by_id",
        _fake_get_by_id,
    )
    monkeypatch.setattr(
        "api.v1.announcements.registration_request_crud.get_all_by_announcement_id",
        _fake_get_rr,
    )

    r = await async_client.get(
        f"/api/v1/games/1/announcements/{a['id']}/registration_requests"
    )
    assert r.status_code == 200
    assert r.json()["data"][0]["announcement_id"] == a["id"]


@pytest.mark.asyncio
async def test_create_update_delete_announcement(
    async_client, create_user, announcement_factory, monkeypatch
):
    user = await create_user(email="creator@example.com", password="pw")
    ann_in = {"title": "T", "content": "C", "game_id": 55}

    created = announcement_factory.build(**ann_in, organizer_id=user.id)

    async def _fake_create(session, announcement_in, user):
        assert announcement_in.title == ann_in["title"]
        return SimpleNamespace(**created)

    monkeypatch.setattr(
        "api.v1.announcements.announcement_crud.create",
        _fake_create,
    )

    async def _cu():
        return user

    import core.users as users_mod

    async_client._transport.app.dependency_overrides[users_mod.current_user] = _cu

    r = await async_client.post(
        f"/api/v1/games/{ann_in['game_id']}/announcements", json=ann_in
    )
    assert r.status_code == 200
    assert r.json()["data"]["title"] == ann_in["title"]

    ann_obj = SimpleNamespace(**created)

    async def _fake_get_by_id_for_edit(
        session, announcement_id, user=None, action=None
    ):
        return ann_obj

    async def _fake_update(session, announcement, announcement_in, user, action=None):
        if hasattr(announcement_in, "model_dump"):
            upd = announcement_in.model_dump()
        elif hasattr(announcement_in, "dict"):
            upd = announcement_in.dict()
        elif isinstance(announcement_in, dict):
            upd = announcement_in
        else:
            try:
                upd = dict(announcement_in)
            except Exception:
                upd = {}

        merged = {**announcement.__dict__, **upd}
        return SimpleNamespace(**merged)

    monkeypatch.setattr(
        "api.v1.announcements.announcement_crud.get_by_id",
        _fake_get_by_id_for_edit,
    )
    monkeypatch.setattr(
        "api.v1.announcements.announcement_crud.update",
        _fake_update,
    )

    updated_payload = {"title": "NewTitle"}
    r = await async_client.patch(
        f"/api/v1/games/{ann_in['game_id']}/announcements/{created['id']}",
        json=updated_payload,
    )
    assert r.status_code == 200
    assert r.json()["data"]["title"] == "NewTitle"

    async def _fake_delete(session, announcement, user, action=None):
        return None

    monkeypatch.setattr(
        "api.v1.announcements.announcement_crud.delete",
        _fake_delete,
    )

    r = await async_client.delete(
        f"/api/v1/games/{ann_in['game_id']}/announcements/{created['id']}"
    )
    assert r.status_code == 200
    assert r.json()["data"] == "Announcement deleted successfully"


@pytest.mark.asyncio
async def test_upload_announcement_image(
    async_client, create_user, announcement_factory, monkeypatch
):
    await create_user(email="img@example.com", password="pw")
    a = announcement_factory.build()
    ann_obj = SimpleNamespace(**a)

    async def _fake_get_by_id_for_edit(
        session, announcement_id, user=None, action=None
    ):
        return ann_obj

    monkeypatch.setattr(
        "api.v1.announcements.announcement_crud.get_by_id",
        _fake_get_by_id_for_edit,
    )

    async def _fake_upload_avatar(**kwargs):
        return "http://img/url.png"

    monkeypatch.setattr("api.v1.announcements.upload_avatar", _fake_upload_avatar)

    from core.db import container as db_container

    class FakeSession:
        async def commit(self):
            return None

        async def refresh(self, obj):
            return None

    async def _fake_session_getter():
        yield FakeSession()

    async_client._transport.app.dependency_overrides[db_container.db.session_getter] = (
        _fake_session_getter
    )

    files = {"file": ("img.png", b"data", "image/png")}

    r = await async_client.post(
        f"/api/v1/games/1/announcements/{a['id']}/upload_image", files=files
    )
    assert r.status_code == 200
    assert r.json()["data"]["image_url"] == "http://img/url.png"
