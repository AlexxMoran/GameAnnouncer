import pytest


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
async def test_get_current_user_and_update(monkeypatch, async_client, create_user):
    user = await create_user(email="me@example.com", password="secret")

    async def _cu():
        return user

    import core.users as users_mod

    async_client._transport.app.dependency_overrides[users_mod.current_user] = _cu

    r = await async_client.get("/api/auth/users/me")
    assert r.status_code == 200

    r = await async_client.patch(
        "/api/auth/users/me", json={"email": "new@example.com"}
    )
    assert r.status_code == 200
    assert r.json()["data"]["email"] == "new@example.com"


@pytest.mark.asyncio
async def test_login_and_logout(monkeypatch, async_client, create_user):
    user = await create_user(email="login@example.com", password="secret")

    monkeypatch.setattr("api.auth.get_jwt_strategy", lambda: FakeStrategy())
    monkeypatch.setattr("api.auth.get_refresh_jwt_strategy", lambda: FakeStrategy(user))

    r = await async_client.post(
        "/api/auth/login", data={"username": "noone", "password": "x"}
    )
    assert r.status_code == 401

    r = await async_client.post(
        "/api/auth/login", data={"username": "login@example.com", "password": "secret"}
    )
    assert r.status_code == 200
    assert "access_token" in r.json()

    r = await async_client.post("/api/auth/logout")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_refresh_token_flow(monkeypatch, async_client, create_user):
    user = await create_user(email="r@example.com", password="secret")

    monkeypatch.setattr("api.auth.get_refresh_jwt_strategy", lambda: FakeStrategy(user))
    monkeypatch.setattr("api.auth.get_jwt_strategy", lambda: FakeStrategy())

    async_client.cookies.set("refresh_token", "any")

    r = await async_client.post("/api/auth/jwt/refresh")
    assert r.status_code == 200
    assert "access_token" in r.json()


@pytest.mark.asyncio
async def test_forgot_and_reset_and_verify(monkeypatch, async_client, create_user):
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
