import pytest
from types import SimpleNamespace


@pytest.mark.asyncio
async def test_get_games_paginated(async_client, game_factory, monkeypatch):
    g1 = game_factory.build()
    g2 = game_factory.build()
    games = [g1, g2]

    class FakeSearch:
        async def results_with_announcements_count(self, skip=0, limit=10):
            return games

        async def count(self):
            return 2

    def _fake_get_game_search(session, filters=None):
        return FakeSearch()

    monkeypatch.setattr("api.v1.games.get_game_search", _fake_get_game_search)
    monkeypatch.setattr("core.deps.get_game_search", _fake_get_game_search)

    import api.v1.games as games_mod

    async_client._transport.app.dependency_overrides[games_mod.get_game_search] = (
        _fake_get_game_search
    )
    monkeypatch.setattr("api.v1.games.get_batch_permissions", lambda user, gs: None)

    async def _fake_results(self, skip=0, limit=10):
        return games

    async def _fake_count(self):
        return 2

    monkeypatch.setattr(
        "searches.game_search.GameSearch.results_with_announcements_count",
        _fake_results,
    )
    monkeypatch.setattr("searches.game_search.GameSearch.count", _fake_count)
    r = await async_client.get("/api/v1/games?skip=0&limit=10")
    assert r.status_code == 200
    body = r.json()

    assert body["total"] == 2
    assert body["limit"] == 10
    assert len(body["data"]) == 2
    assert body["data"][0]["id"] == g1["id"]
    assert body["data"][1]["id"] == g2["id"]


@pytest.mark.asyncio
async def test_get_game_and_permissions(async_client, game_factory, monkeypatch):
    g = game_factory.build()
    g_obj = SimpleNamespace(**g)

    async def _fake_get_by_id(session, game_id):
        return g_obj

    monkeypatch.setattr("api.v1.games.game_crud.get_by_id", _fake_get_by_id)
    monkeypatch.setattr(
        "api.v1.games.get_permissions", lambda user, game: {"edit": True}
    )

    r = await async_client.get(f"/api/v1/games/{g['id']}")
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["id"] == g["id"]
    assert data["permissions"]["edit"] is True


@pytest.mark.asyncio
async def test_get_game_not_found(async_client, game_factory, monkeypatch):
    async def _fake_get_by_id(session, game_id):
        return None

    monkeypatch.setattr("api.v1.games.game_crud.get_by_id", _fake_get_by_id)

    r = await async_client.get("/api/v1/games/9999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_create_game(
    async_client, create_user, game_factory, authenticated_client, monkeypatch
):
    user = await create_user(email="creator@game.test", password="pw")
    game_payload = {"name": "MyGame", "category": "RTS", "description": "d"}

    created = game_factory.build(**game_payload, id=11)

    async def _fake_create(session, game_in, user, action=None):
        assert game_in.name == game_payload["name"]
        return SimpleNamespace(**created)

    monkeypatch.setattr("api.v1.games.game_crud.create", _fake_create)

    client = authenticated_client(user)

    r = await client.post("/api/v1/games", json=game_payload)
    assert r.status_code == 200
    assert r.json()["data"]["name"] == game_payload["name"]


@pytest.mark.asyncio
async def test_update_game_success(
    async_client, create_user, game_factory, authenticated_client, monkeypatch
):
    user = await create_user(email="upd@game.test", password="pw")
    existing = game_factory.build(id=22)
    existing_obj = SimpleNamespace(**existing)

    async def _fake_get_by_id_for_edit(session, game_id, user=None, action=None):
        return existing_obj

    async def _fake_update(session, game, game_in, user, action=None):
        if hasattr(game_in, "model_dump"):
            try:
                upd = game_in.model_dump(exclude_none=True)
            except TypeError:
                upd = game_in.model_dump()
        elif hasattr(game_in, "dict"):
            try:
                upd = game_in.dict(exclude_none=True)
            except TypeError:
                upd = game_in.dict()
        elif isinstance(game_in, dict):
            upd = {k: v for k, v in game_in.items() if v is not None}
        else:
            try:
                upd = dict(game_in)
            except Exception:
                upd = {}

        merged = {**game.__dict__, **(upd or {})}
        return SimpleNamespace(**merged)

    monkeypatch.setattr("api.v1.games.game_crud.get_by_id", _fake_get_by_id_for_edit)
    monkeypatch.setattr("api.v1.games.game_crud.update", _fake_update)

    client = authenticated_client(user)

    payload = {"name": "UpdatedName"}
    r = await client.patch("/api/v1/games/1", json=payload)
    assert r.status_code == 200
    assert r.json()["data"]["name"] == "UpdatedName"


@pytest.mark.asyncio
async def test_update_game_not_found(
    async_client, create_user, authenticated_client, monkeypatch
):
    user = await create_user(email="noexist@g.test", password="pw")

    async def _fake_get_by_id_for_edit(session, game_id, user=None, action=None):
        return None

    monkeypatch.setattr("api.v1.games.game_crud.get_by_id", _fake_get_by_id_for_edit)

    client = authenticated_client(user)

    r = await client.patch("/api/v1/games/999", json={"name": "X"})
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_delete_game_success(
    async_client, create_user, game_factory, authenticated_client, monkeypatch
):
    user = await create_user(email="del@g.test", password="pw")
    existing = game_factory.build(id=33)
    existing_obj = SimpleNamespace(**existing)

    async def _fake_get_by_id_for_edit(session, game_id, user=None, action=None):
        return existing_obj

    async def _fake_delete(session, game, user, action=None):
        return None

    monkeypatch.setattr("api.v1.games.game_crud.get_by_id", _fake_get_by_id_for_edit)
    monkeypatch.setattr("api.v1.games.game_crud.delete", _fake_delete)

    client = authenticated_client(user)

    r = await client.delete("/api/v1/games/1")
    assert r.status_code == 200
    assert r.json()["data"] == "Game deleted successfully"


@pytest.mark.asyncio
async def test_delete_game_not_found(
    async_client, create_user, authenticated_client, monkeypatch
):
    user = await create_user(email="dne@g.test", password="pw")

    async def _fake_get_by_id_for_edit(session, game_id, user=None, action=None):
        return None

    monkeypatch.setattr("api.v1.games.game_crud.get_by_id", _fake_get_by_id_for_edit)

    client = authenticated_client(user)

    r = await client.delete("/api/v1/games/9999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_upload_game_image(async_client, create_user, game_factory, monkeypatch):
    await create_user(email="img@g.test", password="pw")
    g = game_factory.build()
    g_obj = SimpleNamespace(**g)

    async def _fake_get_by_id_for_edit(session, game_id, user=None, action=None):
        return g_obj

    monkeypatch.setattr("api.v1.games.game_crud.get_by_id", _fake_get_by_id_for_edit)

    async def _fake_upload_avatar(**kwargs):
        return "http://img/g.png"

    monkeypatch.setattr("api.v1.games.upload_avatar", _fake_upload_avatar)

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

    r = await async_client.post(f"/api/v1/games/{g['id']}/upload_image", files=files)
    assert r.status_code == 200
    assert r.json()["data"]["image_url"] == "http://img/g.png"
