import pytest
from exceptions.app_exception import AppException
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_get_registration_request_success(
    async_client, registration_request_factory
):
    rr = registration_request_factory.build()

    with patch(
        "api.v1.registration_requests.registration_request_crud.get_by_id",
        new=AsyncMock(return_value=rr),
    ):
        r = await async_client.get(f"/api/v1/registration_requests/{rr['id']}")
        assert r.status_code == 200
        assert r.json()["data"]["id"] == rr["id"]


@pytest.mark.asyncio
async def test_get_registration_request_not_found(async_client):
    with patch(
        "api.v1.registration_requests.registration_request_crud.get_by_id",
        new=AsyncMock(return_value=None),
    ):
        r = await async_client.get("/api/v1/registration_requests/9999")
        assert r.status_code == 404
        assert "Registration Request not found" in r.json().get("detail", "")


@pytest.mark.asyncio
async def test_create_registration_request_success(
    async_client,
    create_user,
    registration_request_factory,
    announcement_factory,
    authenticated_client,
):
    from types import SimpleNamespace

    user = await create_user(email="u@example.com", password="x")
    ann_dict = announcement_factory.build()
    ann_dict["is_registration_open"] = True

    ann = SimpleNamespace(**ann_dict)

    rr_in = {"announcement_id": ann.id}
    with patch(
        "api.v1.registration_requests.get_announcement_dependency",
        new=AsyncMock(return_value=ann),
    ), patch(
        "api.v1.registration_requests.registration_request_crud.get_by_user_and_announcement",
        new=AsyncMock(return_value=None),
    ):
        created = registration_request_factory.build(
            user_id=user.id, announcement_id=ann.id
        )

        async def _fake_service_call():
            return created

        client = authenticated_client(user)

        with patch(
            "api.v1.registration_requests.CreateRegistrationRequestService.call",
            new=AsyncMock(side_effect=_fake_service_call),
        ):
            r = await client.post("/api/v1/registration_requests", json=rr_in)
            assert r.status_code == 200
            assert r.json()["data"]["announcement_id"] == ann.id


@pytest.mark.asyncio
async def test_create_registration_request_duplicate(
    async_client,
    create_user,
    registration_request_factory,
    announcement_factory,
    authenticated_client,
):
    user = await create_user(email="u2@example.com", password="x")
    ann = announcement_factory.build()
    rr_in = {"announcement_id": ann["id"]}

    existing = registration_request_factory.build(
        user_id=user.id, announcement_id=ann["id"]
    )

    with patch(
        "api.v1.registration_requests.get_announcement_dependency",
        new=AsyncMock(return_value=ann),
    ), patch(
        "api.v1.registration_requests.registration_request_crud.get_by_user_and_announcement",
        new=AsyncMock(return_value=existing),
    ):
        client = authenticated_client(user)

        r = await client.post("/api/v1/registration_requests", json=rr_in)
        assert r.status_code == 400
        assert "already exists" in r.json().get("detail", "")


@pytest.mark.asyncio
async def test_create_registration_request_announcement_not_found(
    async_client, create_user, authenticated_client
):
    user = await create_user(email="u3@example.com", password="x")

    with patch(
        "api.v1.registration_requests.get_announcement_dependency",
        new=AsyncMock(
            side_effect=AppException("Announcement not found", status_code=404)
        ),
    ):
        client = authenticated_client(user)

        r = await client.post(
            "/api/v1/registration_requests", json={"announcement_id": 9999}
        )
        assert r.status_code == 404
        assert "Announcement not found" in r.json().get("detail", "")


@pytest.mark.asyncio
async def test_update_registration_request_status_actions(
    async_client,
    create_user,
    registration_request_factory,
    authenticated_client,
):
    user = await create_user(email="actor@example.com", password="x")
    rr = registration_request_factory.build()

    called = {}

    async def _fake_approve(session, registration_request, current_user):
        called["approve"] = True
        return {**registration_request, "status": "approved"}

    async def _fake_reject(
        session, registration_request, current_user, cancellation_reason=None
    ):
        called["reject"] = True
        called["cancellation_reason"] = cancellation_reason
        return {**registration_request, "status": "rejected"}

    async def _fake_cancel(session, registration_request, current_user):
        called["cancel"] = True
        return {**registration_request, "status": "cancelled"}

    client = authenticated_client(user)

    with patch(
        "api.v1.registration_requests.registration_request_crud.get_by_id",
        new=AsyncMock(return_value=rr),
    ), patch(
        "api.v1.registration_requests.registration_request_crud.approve",
        new=AsyncMock(side_effect=_fake_approve),
    ), patch(
        "api.v1.registration_requests.registration_request_crud.reject",
        new=AsyncMock(side_effect=_fake_reject),
    ), patch(
        "api.v1.registration_requests.registration_request_crud.cancel",
        new=AsyncMock(side_effect=_fake_cancel),
    ):
        r = await client.patch(f"/api/v1/registration_requests/{rr['id']}/approve")
        assert r.status_code == 200
        assert r.json()["data"]["status"] == "approved"
        assert called.get("approve")

        r = await client.patch(
            f"/api/v1/registration_requests/{rr['id']}/reject",
            params={"cancellation_reason": "Not suitable"},
        )
        assert r.status_code == 200
        assert r.json()["data"]["status"] == "rejected"
        assert called.get("reject")
        assert called.get("cancellation_reason") == "Not suitable"

        r = await client.patch(f"/api/v1/registration_requests/{rr['id']}/cancel")
        assert r.status_code == 200
        assert r.json()["data"]["status"] == "cancelled"
        assert called.get("cancel")
