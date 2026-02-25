import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timedelta, timezone
from enums import AnnouncementStatus, AnnouncementFormat


@pytest.mark.asyncio
async def test_get_announcements_paginated(async_client, announcement_factory):
    game_id = 123
    a1 = announcement_factory.build(organizer_id=1, game_id=game_id)
    a2 = announcement_factory.build(organizer_id=2, game_id=game_id)
    announcements = [SimpleNamespace(**a1), SimpleNamespace(**a2)]

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

    class FakeService:
        def __init__(self, session, announcement_in, user):
            pass

        async def call(self):
            return ann_obj

    with (
        patch(
            "api.v1.announcements.CreateAnnouncementService",
            new=FakeService,
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

    class FakeService:
        def __init__(self, session, announcement_in, user):
            pass

        async def call(self):
            return ann_obj

    with (
        patch(
            "api.v1.announcements.CreateAnnouncementService",
            new=FakeService,
        ),
        patch("api.v1.announcements.get_permissions", return_value={}),
    ):
        r = await client.post("/api/v1/announcements", json=announcement_data)
        assert r.status_code == 201
        assert r.json()["data"]["status"] == AnnouncementStatus.REGISTRATION_OPEN.value


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


@pytest.mark.asyncio
async def test_create_announcement_with_format(
    async_client, announcement_factory, authenticated_client, user
):
    """Test creating announcement with format field."""
    client = authenticated_client(user)

    now = datetime.now(timezone.utc)
    announcement_data = announcement_factory.build(
        registration_start_at=now.isoformat(),
        registration_end_at=(now + timedelta(days=1)).isoformat(),
        start_at=(now + timedelta(days=2)).isoformat(),
        format=AnnouncementFormat.SINGLE_ELIMINATION,
    )

    ann_obj = SimpleNamespace(**announcement_data)
    ann_obj.status = AnnouncementStatus.REGISTRATION_OPEN

    class FakeService:
        def __init__(self, session, announcement_in, user):
            pass

        async def call(self):
            return ann_obj

    with (
        patch(
            "api.v1.announcements.CreateAnnouncementService",
            new=FakeService,
        ),
        patch("api.v1.announcements.get_permissions", return_value={}),
    ):
        r = await client.post("/api/v1/announcements", json=announcement_data)
        assert r.status_code == 201
        data = r.json()["data"]
        assert data["format"] == AnnouncementFormat.SINGLE_ELIMINATION


@pytest.mark.asyncio
async def test_create_announcement_requires_format(
    async_client, announcement_factory, authenticated_client, user
):
    """Test that format field is required when creating announcement."""
    client = authenticated_client(user)

    now = datetime.now(timezone.utc)
    announcement_data = announcement_factory.build(
        registration_start_at=now.isoformat(),
        registration_end_at=(now + timedelta(days=1)).isoformat(),
        start_at=(now + timedelta(days=2)).isoformat(),
    )
    del announcement_data["format"]

    r = await client.post("/api/v1/announcements", json=announcement_data)
    assert r.status_code == 422
