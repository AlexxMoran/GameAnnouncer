import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_get_games_paginated(async_client, game_factory):
    g1 = game_factory.build()
    g2 = game_factory.build()
    games = [SimpleNamespace(**g1), SimpleNamespace(**g2)]

    with (
        patch(
            "api.v1.games.GameSearch.results",
            new=AsyncMock(return_value=games),
        ),
        patch(
            "api.v1.games.GameSearch.count",
            new=AsyncMock(return_value=2),
        ),
        patch("api.v1.games.get_batch_permissions", return_value=None),
    ):
        r = await async_client.get("/api/v1/games?skip=0&limit=10")
        assert r.status_code == 200
        body = r.json()

        assert body["total"] == 2
        assert body["limit"] == 10
        assert len(body["data"]) == 2
        assert body["data"][0]["id"] == g1["id"]
        assert body["data"][1]["id"] == g2["id"]
