import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timedelta, timezone
from enums import AnnouncementStatus, AnnouncementFormat
from exceptions import AppException, ValidationException


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


@pytest.mark.asyncio
async def test_patch_participant_score_updates_score(
    async_client, announcement_factory, authenticated_client, user
):
    """PATCH participant score returns 200 with updated score."""
    from api.v1.announcements import get_announcement_dependency

    client = authenticated_client(user)

    announcement_data = announcement_factory.build(organizer_id=user.id)
    ann_obj = SimpleNamespace(**announcement_data)

    participant_obj = SimpleNamespace(
        id=7,
        announcement_id=ann_obj.id,
        user_id=99,
        qualification_score=50,
        qualification_rank=None,
        seed=None,
        is_qualified=False,
        created_at=datetime.now(timezone.utc).isoformat(),
        updated_at=datetime.now(timezone.utc).isoformat(),
        user=None,
    )

    async def override_announcement():
        return ann_obj

    app = async_client._transport.app
    app.dependency_overrides[get_announcement_dependency] = override_announcement

    try:
        with patch(
            "api.v1.announcements.update_participant_score",
            new=AsyncMock(return_value=participant_obj),
        ) as mock_service:
            r = await client.patch(
                f"/api/v1/announcements/{ann_obj.id}/participants/7",
                json={"qualification_score": 50},
            )
    finally:
        del app.dependency_overrides[get_announcement_dependency]

    assert r.status_code == 200
    assert r.json()["data"]["qualification_score"] == 50
    mock_service.assert_awaited_once()


@pytest.mark.asyncio
async def test_patch_participant_score_rejects_non_positive_score(
    async_client, announcement_factory, authenticated_client, user
):
    """PATCH participant score returns 422 when score is not a positive integer."""
    from api.v1.announcements import get_announcement_dependency

    client = authenticated_client(user)
    announcement_data = announcement_factory.build()
    ann_obj = SimpleNamespace(**announcement_data)

    async def override_announcement():
        return ann_obj

    app = async_client._transport.app
    app.dependency_overrides[get_announcement_dependency] = override_announcement

    try:
        r = await client.patch(
            f"/api/v1/announcements/{ann_obj.id}/participants/1",
            json={"qualification_score": 0},
        )
    finally:
        del app.dependency_overrides[get_announcement_dependency]

    assert r.status_code == 422


def _make_lifecycle_service_mock(method_name: str, return_value):
    """Build a mock AnnouncementLifecycleService with one async method configured."""
    mock = MagicMock()
    setattr(mock, method_name, AsyncMock(return_value=return_value))
    return mock


@pytest.mark.asyncio
async def test_start_qualification_returns_live_announcement(
    async_client, announcement_factory, authenticated_client, user
):
    """POST /start_qualification returns 200 and transitions announcement to LIVE."""
    from api.v1.announcements import get_announcement_dependency

    client = authenticated_client(user)
    announcement_data = announcement_factory.build(organizer_id=user.id)
    ann_obj = SimpleNamespace(**announcement_data)
    ann_obj.status = AnnouncementStatus.LIVE

    async def override_announcement():
        return ann_obj

    app = async_client._transport.app
    app.dependency_overrides[get_announcement_dependency] = override_announcement

    try:
        with (
            patch("api.v1.announcements.authorize_action"),
            patch(
                "api.v1.announcements.AnnouncementLifecycleService",
                return_value=_make_lifecycle_service_mock(
                    "start_qualification", ann_obj
                ),
            ),
        ):
            r = await client.post(
                f"/api/v1/announcements/{ann_obj.id}/start_qualification"
            )
    finally:
        del app.dependency_overrides[get_announcement_dependency]

    assert r.status_code == 200
    assert r.json()["data"]["status"] == AnnouncementStatus.LIVE.value


@pytest.mark.asyncio
async def test_finalize_qualification_returns_200(
    async_client, announcement_factory, authenticated_client, user
):
    """POST /finalize_qualification returns 200 when announcement is LIVE."""
    from api.v1.announcements import get_announcement_dependency

    client = authenticated_client(user)
    announcement_data = announcement_factory.build(organizer_id=user.id)
    ann_obj = SimpleNamespace(**announcement_data)
    ann_obj.status = AnnouncementStatus.LIVE

    async def override_announcement():
        return ann_obj

    app = async_client._transport.app
    app.dependency_overrides[get_announcement_dependency] = override_announcement

    try:
        with patch(
            "api.v1.announcements.FinalizeQualificationService",
            return_value=MagicMock(call=AsyncMock(return_value=ann_obj)),
        ):
            r = await client.post(
                f"/api/v1/announcements/{ann_obj.id}/finalize_qualification"
            )
    finally:
        del app.dependency_overrides[get_announcement_dependency]

    assert r.status_code == 200
    assert r.json()["data"]["status"] == AnnouncementStatus.LIVE.value


@pytest.mark.asyncio
async def test_generate_bracket_transitions_to_live(
    async_client, announcement_factory, authenticated_client, user
):
    """POST /generate_bracket returns 200 and transitions announcement to LIVE."""
    from api.v1.announcements import get_announcement_dependency

    client = authenticated_client(user)
    announcement_data = announcement_factory.build(organizer_id=user.id)
    ann_obj = SimpleNamespace(**announcement_data)
    ann_obj.status = AnnouncementStatus.LIVE

    async def override_announcement():
        return ann_obj

    app = async_client._transport.app
    app.dependency_overrides[get_announcement_dependency] = override_announcement

    try:
        with (
            patch("api.v1.announcements.authorize_action"),
            patch(
                "api.v1.announcements.AnnouncementLifecycleService",
                return_value=_make_lifecycle_service_mock("generate_bracket", ann_obj),
            ),
        ):
            r = await client.post(
                f"/api/v1/announcements/{ann_obj.id}/generate_bracket"
            )
    finally:
        del app.dependency_overrides[get_announcement_dependency]

    assert r.status_code == 200
    assert r.json()["data"]["status"] == AnnouncementStatus.LIVE.value


@pytest.mark.asyncio
async def test_cancel_announcement_returns_cancelled(
    async_client, announcement_factory, authenticated_client, user
):
    """POST /cancel returns 200 and transitions announcement to CANCELLED."""
    from api.v1.announcements import get_announcement_dependency

    client = authenticated_client(user)
    announcement_data = announcement_factory.build(organizer_id=user.id)
    ann_obj = SimpleNamespace(**announcement_data)
    ann_obj.status = AnnouncementStatus.CANCELLED

    async def override_announcement():
        return ann_obj

    app = async_client._transport.app
    app.dependency_overrides[get_announcement_dependency] = override_announcement

    try:
        with (
            patch("api.v1.announcements.authorize_action"),
            patch(
                "api.v1.announcements.AnnouncementLifecycleService",
                return_value=_make_lifecycle_service_mock("cancel", ann_obj),
            ),
        ):
            r = await client.post(f"/api/v1/announcements/{ann_obj.id}/cancel")
    finally:
        del app.dependency_overrides[get_announcement_dependency]

    assert r.status_code == 200
    assert r.json()["data"]["status"] == AnnouncementStatus.CANCELLED.value


@pytest.mark.asyncio
async def test_lifecycle_endpoint_returns_422_on_invalid_status(
    async_client, announcement_factory, authenticated_client, user
):
    """POST /start_qualification returns 422 when the transition is not allowed."""
    from api.v1.announcements import get_announcement_dependency

    client = authenticated_client(user)
    announcement_data = announcement_factory.build(organizer_id=user.id)
    ann_obj = SimpleNamespace(**announcement_data)

    async def override_announcement():
        return ann_obj

    mock_service = MagicMock()
    mock_service.start_qualification = AsyncMock(
        side_effect=ValidationException(
            "'start_qualification' is not allowed when status is 'live'"
        )
    )

    app = async_client._transport.app
    app.dependency_overrides[get_announcement_dependency] = override_announcement

    try:
        with (
            patch("api.v1.announcements.authorize_action"),
            patch(
                "api.v1.announcements.AnnouncementLifecycleService",
                return_value=mock_service,
            ),
        ):
            r = await client.post(
                f"/api/v1/announcements/{ann_obj.id}/start_qualification"
            )
    finally:
        del app.dependency_overrides[get_announcement_dependency]

    assert r.status_code == 422


@pytest.mark.asyncio
async def test_lifecycle_endpoint_returns_403_for_non_organizer(
    async_client, announcement_factory, authenticated_client, user
):
    """POST /cancel returns 403 when the user is not the organizer."""
    from api.v1.announcements import get_announcement_dependency

    client = authenticated_client(user)
    announcement_data = announcement_factory.build(organizer_id=user.id + 999)
    ann_obj = SimpleNamespace(**announcement_data)

    async def override_announcement():
        return ann_obj

    app = async_client._transport.app
    app.dependency_overrides[get_announcement_dependency] = override_announcement

    try:
        with patch(
            "api.v1.announcements.authorize_action",
            side_effect=AppException("Forbidden", status_code=403),
        ):
            r = await client.post(f"/api/v1/announcements/{ann_obj.id}/cancel")
    finally:
        del app.dependency_overrides[get_announcement_dependency]

    assert r.status_code == 403
