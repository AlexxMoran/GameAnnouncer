import pytest
from unittest.mock import patch


class FakeStrategy:
    def __init__(self, user=None):
        self.user = user

    async def write_token(self, user):
        return f"tok-{user.id}"

    async def read_token(self, token, user_manager):
        return self.user or None


@pytest.mark.asyncio
async def test_register(async_client, user_factory):
    payload = user_factory.build()
    r = await async_client.post("/api/auth/register", params=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["data"]["email"] == payload["email"]


@pytest.mark.asyncio
async def test_get_user_by_id(async_client, create_user):
    user = await create_user(email="getme@example.com", password="secret")
    r = await async_client.get(f"/api/auth/users/{user.id}")
    assert r.status_code == 200
    assert r.json()["data"]["email"] == "getme@example.com"


@pytest.mark.asyncio
async def test_get_current_user_and_update(
    async_client, create_user, authenticated_client
):
    user = await create_user(email="me@example.com", password="secret")

    client = authenticated_client(user)

    r = await client.get("/api/auth/users/me")
    assert r.status_code == 200

    r = await client.patch("/api/auth/users/me", json={"email": "new@example.com"})
    assert r.status_code == 200
    assert r.json()["data"]["email"] == "new@example.com"


@pytest.mark.asyncio
async def test_login_invalid_credentials(async_client, create_user):
    user = await create_user(email="login@example.com", password="secret")
    with (
        patch("api.auth.get_jwt_strategy", return_value=FakeStrategy()),
        patch("api.auth.get_refresh_jwt_strategy", return_value=FakeStrategy(user)),
    ):
        r = await async_client.post(
            "/api/auth/login", data={"username": "noone", "password": "x"}
        )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_login_sets_cookie_and_access_token(async_client, create_user):
    user = await create_user(
        email="login@example.com", password="secret", is_verified=True
    )

    async def fake_authenticate(self, form_data):
        return user

    with (
        patch("core.user_manager.UserManager.authenticate", new=fake_authenticate),
        patch("api.auth.get_jwt_strategy", return_value=FakeStrategy()),
        patch("api.auth.get_refresh_jwt_strategy", return_value=FakeStrategy(user)),
    ):
        r = await async_client.post(
            "/api/auth/login",
            data={"username": "login@example.com", "password": "secret"},
        )

    assert r.status_code == 200
    body = r.json()
    assert "access_token" in body
    assert async_client.cookies.get("refresh_token") is not None


@pytest.mark.asyncio
async def test_logout_clears_cookie(async_client, create_user):
    await create_user(email="login@example.com", password="secret")
    async_client.cookies.set("refresh_token", "someval")
    r = await async_client.post("/api/auth/logout")
    assert r.status_code == 200
    set_cookie = r.headers.get("set-cookie", "")
    assert "refresh_token=" in set_cookie and (
        "Max-Age=0" in set_cookie or "expires=" in set_cookie
    )


@pytest.mark.asyncio
async def test_login_unverified_user_returns_403(async_client):
    unverified = type("U", (), {"id": 1, "is_verified": False})()

    async def fake_authenticate(self, form_data):
        return unverified

    with (
        patch("core.user_manager.UserManager.authenticate", new=fake_authenticate),
        patch("api.auth.get_jwt_strategy", return_value=FakeStrategy()),
        patch(
            "api.auth.get_refresh_jwt_strategy", return_value=FakeStrategy(unverified)
        ),
    ):
        r = await async_client.post(
            "/api/auth/login",
            data={"username": "noone@example.com", "password": "x"},
        )
    assert r.status_code == 403


@pytest.mark.asyncio
async def test_refresh_token_flow(async_client, create_user):
    user = await create_user(email="r@example.com", password="secret")
    with (
        patch("api.auth.get_refresh_jwt_strategy", return_value=FakeStrategy(user)),
        patch("api.auth.get_jwt_strategy", return_value=FakeStrategy()),
    ):
        async_client.cookies.set("refresh_token", "any")

        r = await async_client.post("/api/auth/jwt/refresh")
        assert r.status_code == 200
        assert "access_token" in r.json()


@pytest.mark.asyncio
async def test_forgot_and_reset_and_verify(async_client, create_user):
    await create_user(email="fp@example.com", password="secret")

    r = await async_client.post(
        "/api/auth/forgot-password", params={"email": "fp@example.com"}
    )
    assert r.status_code == 200

    r = await async_client.post(
        "/api/auth/reset-password", params={"token": "bad", "password": "x"}
    )
    assert r.status_code == 400

    r = await async_client.post(
        "/api/auth/request-verify-token", params={"email": "fp@example.com"}
    )
    assert r.status_code == 200

    r = await async_client.post("/api/auth/verify", params={"token": "bad"})
    assert r.status_code == 400
