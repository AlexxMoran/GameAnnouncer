import pytest


@pytest.mark.asyncio
async def test_root(async_client):
    response = await async_client.get("/api/")
    assert response.status_code == 200
    assert "GameAnnouncer API" in response.json()["message"]


@pytest.mark.asyncio
async def test_health(async_client):
    response = await async_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "GameAnnouncer"
    assert "database_url" in data
