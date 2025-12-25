import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_get_announcements_paginated(async_client, announcement_factory):
    game_id = 123
    a1 = announcement_factory.build(organizer_id=1)
    a2 = announcement_factory.build(organizer_id=2)
    announcements = [SimpleNamespace(**a1), SimpleNamespace(**a2)]
    with patch(
        "api.v1.announcements.announcement_crud.get_all_by_game_id",
        new=AsyncMock(return_value=announcements),
    ), patch(
        "api.v1.announcements.announcement_crud.get_all_count_by_game_id",
        new=AsyncMock(return_value=2),
    ), patch(
        "api.v1.announcements.get_batch_permissions", return_value=None
    ):
        r = await async_client.get(
            f"/api/v1/games/{game_id}/announcements?skip=0&limit=10"
        )
        assert r.status_code == 200
        body = r.json()
        assert body["data"][0]["id"] == a1["id"]
        assert body["data"][1]["id"] == a2["id"]
        assert body["skip"] == 0
        assert body["limit"] == 10
        assert body["total"] == 2


@pytest.mark.asyncio
async def test_get_announcement_and_permissions(async_client, announcement_factory):
    a = announcement_factory.build()
    ann_obj = SimpleNamespace(**a)
    with patch(
        "api.v1.announcements.announcement_crud.get_by_id",
        new=AsyncMock(return_value=ann_obj),
    ), patch("api.v1.announcements.get_permissions", return_value={"edit": True}):
        r = await async_client.get(f"/api/v1/games/1/announcements/{a['id']}")
        assert r.status_code == 200
        data = r.json()["data"]
        assert data["id"] == a["id"]
        assert data["organizer_id"] == a["organizer_id"]
        assert data["permissions"]["edit"] is True


@pytest.mark.asyncio
async def test_get_announcement_participants(async_client, announcement_factory):
    a = announcement_factory.build()

    participants = [{"id": 5, "email": "p@example.com"}]

    with patch(
        "api.v1.announcements.announcement_crud.get_by_id",
        new=AsyncMock(return_value=SimpleNamespace(**a)),
    ), patch(
        "api.v1.announcements.announcement_crud.get_participants_by_announcement_id",
        new=AsyncMock(return_value=participants),
    ):
        r = await async_client.get(
            f"/api/v1/games/1/announcements/{a['id']}/participants"
        )
        assert r.status_code == 200
        assert r.json()["data"][0]["email"] == "p@example.com"


@pytest.mark.asyncio
async def test_get_announcement_registration_requests(
    async_client, announcement_factory, registration_request_factory
):
    a = announcement_factory.build()

    fake_rr = [registration_request_factory.build(announcement_id=a["id"])]

    with patch(
        "api.v1.announcements.announcement_crud.get_by_id",
        new=AsyncMock(return_value=SimpleNamespace(**a)),
    ), patch(
        "api.v1.announcements.registration_request_crud.get_all_by_announcement_id",
        new=AsyncMock(return_value=fake_rr),
    ):
        r = await async_client.get(
            f"/api/v1/games/1/announcements/{a['id']}/registration_requests"
        )
        assert r.status_code == 200
        assert r.json()["data"][0]["announcement_id"] == a["id"]


@pytest.mark.asyncio
async def test_create_update_delete_announcement(
    async_client, create_user, announcement_factory, authenticated_client
):
    user = await create_user(email="creator@example.com", password="pw")
    ann_in = {"title": "T", "content": "C", "game_id": 55}

    created = announcement_factory.build(**ann_in, organizer_id=user.id)

    async def _fake_create(session, announcement_in, user):
        assert announcement_in.title == ann_in["title"]
        return SimpleNamespace(**created)

    client = authenticated_client(user)

    with patch(
        "api.v1.announcements.announcement_crud.create",
        new=AsyncMock(side_effect=_fake_create),
    ):
        r = await client.post(
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

    with patch(
        "api.v1.announcements.announcement_crud.get_by_id",
        new=AsyncMock(side_effect=_fake_get_by_id_for_edit),
    ), patch("api.v1.announcements.announcement_crud.update", new=_fake_update):
        updated_payload = {"title": "NewTitle"}
        r = await client.patch(
            f"/api/v1/games/{ann_in['game_id']}/announcements/{created['id']}",
            json=updated_payload,
        )
        assert r.status_code == 200
        assert r.json()["data"]["title"] == "NewTitle"

    async def _fake_delete(session, announcement, user, action=None):
        return None

    with patch(
        "api.v1.announcements.announcement_crud.get_by_id",
        new=AsyncMock(return_value=ann_obj),
    ), patch(
        "api.v1.announcements.announcement_crud.delete",
        new=AsyncMock(side_effect=_fake_delete),
    ):
        r = await client.delete(
            f"/api/v1/games/{ann_in['game_id']}/announcements/{created['id']}"
        )
        assert r.status_code == 200
        assert r.json()["data"] == "Announcement deleted successfully"


@pytest.mark.asyncio
async def test_upload_announcement_image(
    async_client, create_user, announcement_factory
):
    await create_user(email="img@example.com", password="pw")
    a = announcement_factory.build()
    ann_obj = SimpleNamespace(**a)

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

    with patch(
        "api.v1.announcements.announcement_crud.get_by_id",
        new=AsyncMock(return_value=ann_obj),
    ), patch(
        "api.v1.announcements.upload_avatar",
        new=AsyncMock(return_value="http://img/url.png"),
    ):
        files = {"file": ("img.png", b"data", "image/png")}

        r = await async_client.post(
            f"/api/v1/games/1/announcements/{a['id']}/upload_image", files=files
        )
        assert r.status_code == 200
        assert r.json()["data"]["image_url"] == "http://img/url.png"
