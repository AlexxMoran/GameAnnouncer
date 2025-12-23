import pytest
from exceptions.app_exception import AppException


@pytest.mark.asyncio
async def test_get_registration_request_success(
    async_client, registration_request_factory, monkeypatch
):
    rr = registration_request_factory.build()

    async def _fake_get_by_id(session, registration_request_id):
        return rr

    monkeypatch.setattr(
        "api.v1.registration_requests.registration_request_crud.get_by_id",
        _fake_get_by_id,
    )

    r = await async_client.get(f"/api/v1/registration_requests/{rr['id']}")
    assert r.status_code == 200
    assert r.json()["data"]["id"] == rr["id"]


@pytest.mark.asyncio
async def test_get_registration_request_not_found(async_client, monkeypatch):
    async def _fake_get_by_id(session, registration_request_id):
        return None

    monkeypatch.setattr(
        "api.v1.registration_requests.registration_request_crud.get_by_id",
        _fake_get_by_id,
    )

    r = await async_client.get("/api/v1/registration_requests/9999")
    assert r.status_code == 404
    assert "Registration Request not found" in r.json().get("detail", "")


@pytest.mark.asyncio
async def test_create_registration_request_success(
    async_client,
    create_user,
    registration_request_factory,
    announcement_factory,
    monkeypatch,
):
    user = await create_user(email="u@example.com", password="x")
    ann = announcement_factory.build()
    rr_in = {"announcement_id": ann["id"]}

    async def _fake_get_announcement_dependency(session, announcement_id):
        return ann

    monkeypatch.setattr(
        "api.v1.registration_requests.get_announcement_dependency",
        _fake_get_announcement_dependency,
    )

    async def _fake_get_by_user_and_announcement(session, user_id, announcement_id):
        return None

    monkeypatch.setattr(
        "api.v1.registration_requests.registration_request_crud.get_by_user_and_announcement",
        _fake_get_by_user_and_announcement,
    )

    created = registration_request_factory.build(
        user_id=user.id, announcement_id=ann["id"]
    )

    async def _fake_create(session, registration_request_in, user: object):
        return created

    monkeypatch.setattr(
        "api.v1.registration_requests.registration_request_crud.create",
        _fake_create,
    )

    async def _cu():
        return user

    import core.users as users_mod

    async_client._transport.app.dependency_overrides[users_mod.current_user] = _cu

    r = await async_client.post("/api/v1/registration_requests", json=rr_in)
    assert r.status_code == 200
    assert r.json()["data"]["announcement_id"] == ann["id"]


@pytest.mark.asyncio
async def test_create_registration_request_duplicate(
    async_client,
    create_user,
    registration_request_factory,
    announcement_factory,
    monkeypatch,
):
    user = await create_user(email="u2@example.com", password="x")
    ann = announcement_factory.build()
    rr_in = {"announcement_id": ann["id"]}

    async def _fake_get_announcement_dependency(session, announcement_id):
        return ann

    monkeypatch.setattr(
        "api.v1.registration_requests.get_announcement_dependency",
        _fake_get_announcement_dependency,
    )

    existing = registration_request_factory.build(
        user_id=user.id, announcement_id=ann["id"]
    )

    async def _fake_get_by_user_and_announcement(session, user_id, announcement_id):
        return existing

    monkeypatch.setattr(
        "api.v1.registration_requests.registration_request_crud.get_by_user_and_announcement",
        _fake_get_by_user_and_announcement,
    )

    async def _cu():
        return user

    import core.users as users_mod

    async_client._transport.app.dependency_overrides[users_mod.current_user] = _cu

    r = await async_client.post("/api/v1/registration_requests", json=rr_in)
    assert r.status_code == 400
    assert "already exists" in r.json().get("detail", "")


@pytest.mark.asyncio
async def test_create_registration_request_announcement_not_found(
    async_client, create_user, monkeypatch
):
    user = await create_user(email="u3@example.com", password="x")

    async def _fake_get_announcement_dependency(session, announcement_id):
        raise AppException("Announcement not found", status_code=404)

    monkeypatch.setattr(
        "api.v1.registration_requests.get_announcement_dependency",
        _fake_get_announcement_dependency,
    )

    async def _cu():
        return user

    import core.users as users_mod

    async_client._transport.app.dependency_overrides[users_mod.current_user] = _cu

    r = await async_client.post(
        "/api/v1/registration_requests", json={"announcement_id": 9999}
    )
    assert r.status_code == 404
    assert "Announcement not found" in r.json().get("detail", "")


@pytest.mark.asyncio
async def test_update_registration_request_status_actions(
    async_client, create_user, registration_request_factory, monkeypatch
):
    user = await create_user(email="actor@example.com", password="x")
    rr = registration_request_factory.build()

    async def _fake_get_by_id(session, registration_request_id):
        return rr

    monkeypatch.setattr(
        "api.v1.registration_requests.registration_request_crud.get_by_id",
        _fake_get_by_id,
    )

    called = {}

    async def _fake_approve(session, registration_request, current_user):
        called["approve"] = True
        return {**registration_request, "status": "approved"}

    async def _fake_reject(session, registration_request, current_user):
        called["reject"] = True
        return {**registration_request, "status": "rejected"}

    async def _fake_cancel(session, registration_request, current_user):
        called["cancel"] = True
        return {**registration_request, "status": "cancelled"}

    monkeypatch.setattr(
        "api.v1.registration_requests.registration_request_crud.approve",
        _fake_approve,
    )
    monkeypatch.setattr(
        "api.v1.registration_requests.registration_request_crud.reject",
        _fake_reject,
    )
    monkeypatch.setattr(
        "api.v1.registration_requests.registration_request_crud.cancel",
        _fake_cancel,
    )

    async def _cu():
        return user

    import core.users as users_mod

    async_client._transport.app.dependency_overrides[users_mod.current_user] = _cu

    r = await async_client.patch(f"/api/v1/registration_requests/{rr['id']}/approve")
    assert r.status_code == 200
    assert r.json()["data"]["status"] == "approved"
    assert called.get("approve")

    r = await async_client.patch(f"/api/v1/registration_requests/{rr['id']}/reject")
    assert r.status_code == 200
    assert r.json()["data"]["status"] == "rejected"
    assert called.get("reject")

    r = await async_client.patch(f"/api/v1/registration_requests/{rr['id']}/cancel")
    assert r.status_code == 200
    assert r.json()["data"]["status"] == "cancelled"
    assert called.get("cancel")
