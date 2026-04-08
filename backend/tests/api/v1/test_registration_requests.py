import pytest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from domains.participants.schemas import AnnouncementParticipantResponse


def _make_fake_game(**overrides) -> SimpleNamespace:
    data = {"id": 1, "name": "CS2", "image_url": None, "category": "FPS"}
    data.update(overrides)
    return SimpleNamespace(**data)


def _make_fake_announcement(**overrides) -> SimpleNamespace:
    data = {
        "id": 1,
        "title": "Spring Cup",
        "content": None,
        "format": "single_elimination",
        "registration_end_at": datetime.now(timezone.utc),
        "game": _make_fake_game(),
        "participants": [],
    }
    data.update(overrides)
    return SimpleNamespace(**data)


def _make_fake_user(**overrides) -> SimpleNamespace:
    data = {
        "id": 1,
        "first_name": "Alex",
        "last_name": "Moran",
        "nickname": "caster",
        "avatar_icon_id": 7,
        "avatar_color": "#AABBCC",
    }
    data.update(overrides)
    return SimpleNamespace(**data)


def _make_fake_rr(**overrides) -> SimpleNamespace:
    ann = overrides.pop("announcement", _make_fake_announcement())
    user_id = overrides.get("user_id")
    user = overrides.pop("user", None)
    if user is None:
        user = _make_fake_user(id=user_id or 1)
    elif user_id is not None:
        user = SimpleNamespace(**{**vars(user), "id": user_id})
    data = {
        "id": 1,
        "announcement_id": ann.id,
        "user_id": user.id,
        "user": user,
        "status": "pending",
        "cancellation_reason": None,
        "form_responses": [],
        "announcement": ann,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    data.update(overrides)
    return SimpleNamespace(**data)


@pytest.mark.asyncio
async def test_get_registration_request_includes_announcement(
    async_client, authenticated_client, user
):
    """GET /{id} response must include announcement with nested game."""
    client = authenticated_client(user)
    fake_rr = _make_fake_rr(user_id=user.id)

    import api.v1.registration_requests as rr_module

    async def _fake_dep(registration_request_id: int, session=None):
        return fake_rr

    client._transport.app.dependency_overrides[
        rr_module.get_registration_request_dependency
    ] = _fake_dep
    try:
        with patch("api.v1.registration_requests.authorize_action"):
            r = await client.get("/api/v1/registration_requests/1")
    finally:
        client._transport.app.dependency_overrides.pop(
            rr_module.get_registration_request_dependency, None
        )

    assert r.status_code == 200
    data = r.json()["data"]
    assert data["announcement"]["id"] == fake_rr.announcement.id
    assert data["announcement"]["title"] == "Spring Cup"
    assert data["announcement"]["game"]["name"] == "CS2"
    assert data["announcement"]["game"]["category"] == "FPS"
    assert data["user"]["id"] == user.id
    assert data["user_id"] == user.id
    assert "participants_count" in data["announcement"]


@pytest.mark.asyncio
async def test_get_registration_request_announcement_participants_count(
    async_client, authenticated_client, user
):
    """participants_count in announcement reflects the participants list length."""
    client = authenticated_client(user)
    participants = [
        AnnouncementParticipantResponse(
            id=n,
            announcement_id=1,
            user_id=n,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        for n in range(1, 4)
    ]
    ann = _make_fake_announcement(participants=participants)
    fake_rr = _make_fake_rr(user_id=user.id, announcement=ann)

    import api.v1.registration_requests as rr_module

    async def _fake_dep(registration_request_id: int, session=None):
        return fake_rr

    client._transport.app.dependency_overrides[
        rr_module.get_registration_request_dependency
    ] = _fake_dep
    try:
        with patch("api.v1.registration_requests.authorize_action"):
            r = await client.get("/api/v1/registration_requests/1")
    finally:
        client._transport.app.dependency_overrides.pop(
            rr_module.get_registration_request_dependency, None
        )

    assert r.status_code == 200
    assert r.json()["data"]["announcement"]["participants_count"] == 3
    assert r.json()["data"]["user"]["id"] == user.id


@pytest.mark.asyncio
async def test_create_registration_request_includes_announcement(
    async_client, authenticated_client, user
):
    """POST / response must include announcement with nested game."""
    client = authenticated_client(user)

    fake_rr_before = _make_fake_rr(user_id=user.id, id=42)
    fake_rr_after = _make_fake_rr(user_id=user.id, id=42)
    fake_announcement = _make_fake_announcement(id=10)

    class FakeCreateService:
        def __init__(self, **kwargs):
            pass

        async def call(self):
            return fake_rr_before

    with (
        patch("api.v1.registration_requests.AnnouncementRepository") as MockAnnRepo,
        patch(
            "api.v1.registration_requests.CreateRegistrationRequestService",
            new=FakeCreateService,
        ),
        patch(
            "api.v1.registration_requests.RegistrationRequestRepository"
        ) as MockRRRepo,
    ):
        mock_ann_repo = AsyncMock()
        mock_ann_repo.find_by_id.return_value = fake_announcement
        MockAnnRepo.return_value = mock_ann_repo

        mock_rr_repo = AsyncMock()
        mock_rr_repo.find_by_id.return_value = fake_rr_after
        MockRRRepo.return_value = mock_rr_repo

        r = await client.post(
            "/api/v1/registration_requests",
            json={"announcement_id": 10, "form_responses": []},
        )

    assert r.status_code == 200
    data = r.json()["data"]
    assert data["announcement"]["id"] == fake_rr_after.announcement.id
    assert data["announcement"]["game"]["name"] == "CS2"
    assert data["user"]["id"] == user.id
    assert data["user_id"] == user.id
    assert "participants_count" in data["announcement"]


@pytest.mark.asyncio
async def test_cancel_registration_request_includes_announcement(
    async_client, authenticated_client, user
):
    """PATCH /{id}/cancel response must include announcement with nested game."""
    client = authenticated_client(user)
    fake_rr = _make_fake_rr(user_id=user.id, status="pending", id=5)
    fake_rr_after = _make_fake_rr(user_id=user.id, status="cancelled", id=5)

    import api.v1.registration_requests as rr_module

    async def _fake_dep(registration_request_id: int, session=None):
        return fake_rr

    client._transport.app.dependency_overrides[
        rr_module.get_registration_request_dependency
    ] = _fake_dep
    try:
        with (
            patch("api.v1.registration_requests.authorize_action"),
            patch(
                "api.v1.registration_requests.RegistrationRequestRepository"
            ) as MockRRRepo,
            patch(
                "api.v1.registration_requests.RegistrationLifecycleService"
            ) as MockLifecycle,
        ):
            mock_lifecycle = AsyncMock()
            mock_lifecycle.cancel.return_value = fake_rr
            MockLifecycle.return_value = mock_lifecycle

            mock_rr_repo = AsyncMock()
            mock_rr_repo.find_by_id.return_value = fake_rr_after
            MockRRRepo.return_value = mock_rr_repo

            r = await client.patch("/api/v1/registration_requests/5/cancel")
    finally:
        client._transport.app.dependency_overrides.pop(
            rr_module.get_registration_request_dependency, None
        )

    assert r.status_code == 200
    data = r.json()["data"]
    assert data["status"] == "cancelled"
    assert data["announcement"]["id"] == fake_rr_after.announcement.id
    assert data["announcement"]["game"]["name"] == "CS2"
    assert data["user"]["id"] == user.id
    assert data["user_id"] == user.id
