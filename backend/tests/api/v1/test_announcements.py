import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timedelta, timezone
from enums import AnnouncementStatus


@pytest.mark.asyncio
async def test_get_announcements_paginated(async_client, announcement_factory):
    game_id = 123
    a1 = announcement_factory.build(organizer_id=1, game_id=game_id)
    a2 = announcement_factory.build(organizer_id=2, game_id=game_id)
    announcements = [SimpleNamespace(**a1), SimpleNamespace(**a2)]

    # Mock AnnouncementSearch
    mock_search = MagicMock()
    mock_search.results = AsyncMock(return_value=announcements)
    mock_search.count = AsyncMock(return_value=2)

    with (
        patch("api.v1.announcements.AnnouncementSearch", return_value=mock_search),
        patch("api.v1.announcements.get_batch_permissions", return_value=None),
    ):
        r = await async_client.get(
            f"/api/v1/announcements?game_id={game_id}&skip=0&limit=10"
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
    with (
        patch(
            "api.v1.announcements.announcement_crud.get_by_id",
            new=AsyncMock(return_value=ann_obj),
        ),
        patch("api.v1.announcements.get_permissions", return_value={"edit": True}),
    ):
        r = await async_client.get(f"/api/v1/announcements/{a['id']}")
        assert r.status_code == 200
        data = r.json()["data"]
        assert data["id"] == a["id"]
        assert data["organizer_id"] == a["organizer_id"]
        assert data["permissions"]["edit"] is True


@pytest.mark.asyncio
async def test_get_announcement_includes_participants_count(
    async_client, announcement_factory
):
    participants = [{"id": 1}, {"id": 2}, {"id": 3}]
    a = announcement_factory.build(participants=participants)
    ann_obj = SimpleNamespace(**a)

    with (
        patch(
            "api.v1.announcements.announcement_crud.get_by_id",
            new=AsyncMock(return_value=ann_obj),
        ),
        patch("api.v1.announcements.get_permissions", return_value={}),
    ):
        r = await async_client.get(f"/api/v1/announcements/{a['id']}")
        assert r.status_code == 200
        data = r.json()["data"]
        assert data["participants_count"] == 3
        assert "participants" not in data


@pytest.mark.asyncio
async def test_get_announcement_participants(async_client, announcement_factory):
    a = announcement_factory.build()

    participants = [{"id": 5, "email": "p@example.com"}]

    with (
        patch(
            "api.v1.announcements.announcement_crud.get_by_id",
            new=AsyncMock(return_value=SimpleNamespace(**a)),
        ),
        patch(
            "api.v1.announcements.announcement_crud.get_participants_by_announcement_id",
            new=AsyncMock(return_value=(participants, len(participants))),
        ),
    ):
        r = await async_client.get(f"/api/v1/announcements/{a['id']}/participants")
        assert r.status_code == 200
        response_data = r.json()
        assert response_data["data"][0]["email"] == "p@example.com"
        assert response_data["total"] == 1
        assert response_data["skip"] == 0
        assert response_data["limit"] == 10


@pytest.mark.asyncio
async def test_get_announcement_registration_requests(
    async_client, announcement_factory, registration_request_factory
):
    a = announcement_factory.build()

    fake_rr = [registration_request_factory.build(announcement_id=a["id"])]

    with (
        patch(
            "api.v1.announcements.announcement_crud.get_by_id",
            new=AsyncMock(return_value=SimpleNamespace(**a)),
        ),
        patch(
            "api.v1.announcements.registration_request_crud.get_all_by_announcement_id",
            new=AsyncMock(return_value=(fake_rr, len(fake_rr))),
        ),
    ):
        r = await async_client.get(
            f"/api/v1/announcements/{a['id']}/registration_requests"
        )
        assert r.status_code == 200
        response_data = r.json()
        assert response_data["data"][0]["announcement_id"] == a["id"]
        assert response_data["total"] == 1
        assert response_data["skip"] == 0
        assert response_data["limit"] == 10


@pytest.mark.asyncio
async def test_create_update_delete_announcement(
    async_client, create_user, announcement_factory, authenticated_client
):
    user = await create_user(email="creator@example.com", password="pw")
    now = datetime.now(timezone.utc)
    ann_in = {
        "title": "T",
        "content": "C",
        "game_id": 55,
        "start_at": (now + timedelta(days=3)).isoformat(),
        "registration_start_at": now.isoformat(),
        "registration_end_at": (now + timedelta(days=2)).isoformat(),
        "max_participants": 10,
    }

    created = announcement_factory.build(**ann_in, organizer_id=user.id)

    class FakeService:
        def __init__(self, session, announcement_in, user):
            assert announcement_in.title == ann_in["title"]

        async def call(self):
            return SimpleNamespace(**created)

    client = authenticated_client(user)

    with patch(
        "api.v1.announcements.CreateAnnouncementService",
        new=FakeService,
    ):
        r = await client.post("/api/v1/announcements", json=ann_in)
        assert r.status_code == 201
        assert r.json()["data"]["title"] == ann_in["title"]

    ann_obj = SimpleNamespace(**created)

    async def _fake_get_by_id_for_edit(
        session, announcement_id, user=None, action=None
    ):
        return ann_obj

    async def _fake_update(session, announcement, announcement_in, user, action=None):
        if hasattr(announcement_in, "model_dump"):
            upd = announcement_in.model_dump(exclude_unset=True)
        elif hasattr(announcement_in, "dict"):
            upd = announcement_in.dict(exclude_unset=True)
        elif isinstance(announcement_in, dict):
            upd = announcement_in
        else:
            try:
                upd = dict(announcement_in)
            except Exception:
                upd = {}

        merged = {**announcement.__dict__, **upd}
        return SimpleNamespace(**merged)

    with (
        patch(
            "api.v1.announcements.announcement_crud.get_by_id",
            new=AsyncMock(side_effect=_fake_get_by_id_for_edit),
        ),
        patch("api.v1.announcements.announcement_crud.update", new=_fake_update),
    ):
        updated_payload = {"title": "NewTitle", "max_participants": 10}
        r = await client.patch(
            f"/api/v1/announcements/{created['id']}",
            json=updated_payload,
        )
        assert r.status_code == 200
        assert r.json()["data"]["title"] == "NewTitle"

    async def _fake_delete(session, announcement, user, action=None):
        return None

    with (
        patch(
            "api.v1.announcements.announcement_crud.get_by_id",
            new=AsyncMock(return_value=ann_obj),
        ),
        patch(
            "api.v1.announcements.announcement_crud.delete",
            new=AsyncMock(side_effect=_fake_delete),
        ),
    ):
        r = await client.delete(f"/api/v1/announcements/{created['id']}")
        assert r.status_code == 200
        assert r.json()["data"] == "Announcement deleted successfully"


@pytest.mark.asyncio
async def test_upload_announcement_image(
    async_client, create_user, announcement_factory
):
    await create_user(email="img@example.com", password="pw")
    a = announcement_factory.build()
    ann_obj = SimpleNamespace(**a)

    from core import deps as core_deps

    class FakeSession:
        async def commit(self):
            return None

        async def refresh(self, obj):
            return None

    async def _fake_session_getter():
        yield FakeSession()

    async_client._transport.app.dependency_overrides[core_deps._session_getter_dep] = (
        _fake_session_getter
    )

    with (
        patch(
            "api.v1.announcements.announcement_crud.get_by_id",
            new=AsyncMock(return_value=ann_obj),
        ),
        patch(
            "api.v1.announcements.upload_avatar",
            new=AsyncMock(return_value="http://img/url.png"),
        ),
    ):
        files = {"file": ("img.png", b"data", "image/png")}

        r = await async_client.post(
            f"/api/v1/announcements/{a['id']}/upload_image", files=files
        )
        assert r.status_code == 200
        assert r.json()["data"]["image_url"] == "http://img/url.png"


@pytest.mark.asyncio
async def test_create_announcement_sets_pre_registration_status(
    async_client, announcement_factory, authenticated_client, user
):
    """Тест: статус PRE_REGISTRATION когда registration_start_at в будущем."""
    client = authenticated_client(user)

    future_start = datetime.now(timezone.utc) + timedelta(hours=2)
    announcement_data = announcement_factory.build(
        registration_start_at=future_start.isoformat(),
        registration_end_at=(future_start + timedelta(days=1)).isoformat(),
        start_at=(future_start + timedelta(days=2)).isoformat(),
    )

    ann_obj = SimpleNamespace(**announcement_data)
    ann_obj.status = AnnouncementStatus.PRE_REGISTRATION

    with (
        patch(
            "api.v1.announcements.announcement_crud.create",
            new=AsyncMock(return_value=ann_obj),
        ),
        patch("api.v1.announcements.get_permissions", return_value={}),
    ):
        r = await client.post("/api/v1/announcements", json=announcement_data)
        assert r.status_code == 201
        assert r.json()["data"]["status"] == AnnouncementStatus.PRE_REGISTRATION.value


@pytest.mark.asyncio
async def test_create_announcement_sets_registration_open_status(
    async_client, announcement_factory, authenticated_client, user
):
    client = authenticated_client(user)

    past_start = datetime.now(timezone.utc) - timedelta(hours=1)
    announcement_data = announcement_factory.build(
        registration_start_at=past_start.isoformat(),
        registration_end_at=(past_start + timedelta(days=1)).isoformat(),
        start_at=(past_start + timedelta(days=2)).isoformat(),
    )

    ann_obj = SimpleNamespace(**announcement_data)
    ann_obj.status = AnnouncementStatus.REGISTRATION_OPEN

    with (
        patch(
            "api.v1.announcements.announcement_crud.create",
            new=AsyncMock(return_value=ann_obj),
        ),
        patch("api.v1.announcements.get_permissions", return_value={}),
    ):
        r = await client.post("/api/v1/announcements", json=announcement_data)
        assert r.status_code == 201
        assert r.json()["data"]["status"] == AnnouncementStatus.REGISTRATION_OPEN.value


@pytest.mark.asyncio
async def test_update_status_finish_from_live(
    async_client, announcement_factory, authenticated_client, user
):
    client = authenticated_client(user)

    announcement_data = announcement_factory.build(status=AnnouncementStatus.LIVE.value)
    ann_obj = SimpleNamespace(**announcement_data)
    ann_obj.status = AnnouncementStatus.LIVE

    finished_obj = SimpleNamespace(**announcement_data)
    finished_obj.status = AnnouncementStatus.FINISHED

    with (
        patch(
            "api.v1.announcements.announcement_crud.get_by_id",
            new=AsyncMock(return_value=ann_obj),
        ),
        patch(
            "api.v1.announcements.announcement_crud.update_status",
            new=AsyncMock(return_value=finished_obj),
        ),
        patch("api.v1.announcements.get_permissions", return_value={}),
    ):
        r = await client.patch(
            f"/api/v1/announcements/{announcement_data['id']}/status",
            json={"action": "finish"},
        )
        assert r.status_code == 200
        assert r.json()["data"]["status"] == AnnouncementStatus.FINISHED.value


@pytest.mark.asyncio
async def test_update_status_finish_from_wrong_status_fails(
    async_client, announcement_factory, authenticated_client, user
):
    client = authenticated_client(user)

    announcement_data = announcement_factory.build(
        status=AnnouncementStatus.REGISTRATION_OPEN.value
    )
    ann_obj = SimpleNamespace(**announcement_data)
    ann_obj.status = AnnouncementStatus.REGISTRATION_OPEN

    from exceptions import ValidationException

    with (
        patch(
            "api.v1.announcements.announcement_crud.get_by_id",
            new=AsyncMock(return_value=ann_obj),
        ),
        patch(
            "api.v1.announcements.announcement_crud.update_status",
            new=AsyncMock(
                side_effect=ValidationException(
                    "Can only finish announcement when it is 'live'"
                )
            ),
        ),
    ):
        r = await client.patch(
            f"/api/v1/announcements/{announcement_data['id']}/status",
            json={"action": "finish"},
        )
        assert r.status_code == 422


@pytest.mark.asyncio
async def test_update_status_cancel_from_any_status(
    async_client, announcement_factory, authenticated_client, user
):
    client = authenticated_client(user)

    announcement_data = announcement_factory.build(
        status=AnnouncementStatus.PRE_REGISTRATION.value
    )
    ann_obj = SimpleNamespace(**announcement_data)
    ann_obj.status = AnnouncementStatus.PRE_REGISTRATION

    cancelled_obj = SimpleNamespace(**announcement_data)
    cancelled_obj.status = AnnouncementStatus.CANCELLED

    with (
        patch(
            "api.v1.announcements.announcement_crud.get_by_id",
            new=AsyncMock(return_value=ann_obj),
        ),
        patch(
            "api.v1.announcements.announcement_crud.update_status",
            new=AsyncMock(return_value=cancelled_obj),
        ),
        patch("api.v1.announcements.get_permissions", return_value={}),
    ):
        r = await client.patch(
            f"/api/v1/announcements/{announcement_data['id']}/status",
            json={"action": "cancel"},
        )
        assert r.status_code == 200
        assert r.json()["data"]["status"] == AnnouncementStatus.CANCELLED.value


@pytest.mark.asyncio
async def test_get_announcements_with_game_filter(async_client, announcement_factory):
    game_id = 999
    a1 = announcement_factory.build(game_id=game_id)
    a2 = announcement_factory.build(game_id=game_id)
    announcements = [SimpleNamespace(**a1), SimpleNamespace(**a2)]

    mock_search = MagicMock()
    mock_search.results = AsyncMock(return_value=announcements)
    mock_search.count = AsyncMock(return_value=2)

    with (
        patch("api.v1.announcements.AnnouncementSearch", return_value=mock_search),
        patch("api.v1.announcements.get_batch_permissions", return_value=None),
    ):
        r = await async_client.get(f"/api/v1/announcements?game_id={game_id}")
        assert r.status_code == 200
        body = r.json()
        assert body["total"] == 2
        assert all(item["game_id"] == game_id for item in body["data"])


@pytest.mark.asyncio
async def test_get_all_announcements_without_filter(async_client, announcement_factory):
    a1 = announcement_factory.build(game_id=1)
    a2 = announcement_factory.build(game_id=2)
    a3 = announcement_factory.build(game_id=3)
    announcements = [
        SimpleNamespace(**a1),
        SimpleNamespace(**a2),
        SimpleNamespace(**a3),
    ]

    mock_search = MagicMock()
    mock_search.results = AsyncMock(return_value=announcements)
    mock_search.count = AsyncMock(return_value=3)

    with (
        patch("api.v1.announcements.AnnouncementSearch", return_value=mock_search),
        patch("api.v1.announcements.get_batch_permissions", return_value=None),
    ):
        r = await async_client.get("/api/v1/announcements")
        assert r.status_code == 200
        body = r.json()
        assert body["total"] == 3
        assert len(body["data"]) == 3
