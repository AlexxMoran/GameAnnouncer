import pytest
from datetime import datetime, timezone


@pytest.mark.asyncio
async def test_get_my_organized_announcements(
    async_client, create_user, announcement_factory, authenticated_client, monkeypatch
):
    user = await create_user(email="org@example.com", password="secret")

    fake_announcements = [announcement_factory.build(organizer_id=user.id)]

    called = {}

    async def _fake_get_all_by_organizer_id(session, organizer_id, skip=0, limit=10):
        called["organizer_id"] = organizer_id
        called["skip"] = skip
        called["limit"] = limit
        return fake_announcements

    monkeypatch.setattr(
        "api.v1.users.announcement_crud.get_all_by_organizer_id",
        _fake_get_all_by_organizer_id,
    )

    client = authenticated_client(user)

    r = await client.get("/api/v1/users/me/organized_announcements?skip=2&limit=5")
    assert r.status_code == 200
    data = r.json()["data"]
    assert isinstance(data, list)
    assert data[0]["title"] == fake_announcements[0]["title"]
    assert called["organizer_id"] == user.id
    assert called["skip"] == 2
    assert called["limit"] == 5


@pytest.mark.asyncio
async def test_get_my_participated_announcements(
    async_client, create_user, announcement_factory, authenticated_client, monkeypatch
):
    user = await create_user(email="part@example.com", password="secret")

    fake_announcements = [announcement_factory.build(organizer_id=999)]

    called = {}

    async def _fake_get_all_by_participant_id(
        session, participant_id, skip=0, limit=10
    ):
        called["participant_id"] = participant_id
        called["skip"] = skip
        called["limit"] = limit
        return fake_announcements

    monkeypatch.setattr(
        "api.v1.users.announcement_crud.get_all_by_participant_id",
        _fake_get_all_by_participant_id,
    )

    authenticated_client(user)

    r = await async_client.get(
        "/api/v1/users/me/participated_announcements?skip=1&limit=2"
    )
    assert r.status_code == 200
    data = r.json()["data"]
    assert data[0]["title"] == fake_announcements[0]["title"]
    assert called["participant_id"] == user.id
    assert called["skip"] == 1
    assert called["limit"] == 2


@pytest.mark.asyncio
async def test_get_my_registration_requests(
    async_client,
    create_user,
    registration_request_factory,
    authenticated_client,
    monkeypatch,
):
    user = await create_user(email="rr@example.com", password="secret")

    datetime.now(timezone.utc).isoformat()

    fake_requests = [
        registration_request_factory.build(user_id=user.id, announcement_id=5)
    ]

    called = {}

    async def _fake_get_all_by_user_id(session, user_id, skip=0, limit=10):
        called["user_id"] = user_id
        called["skip"] = skip
        called["limit"] = limit
        return fake_requests

    monkeypatch.setattr(
        "api.v1.users.registration_request_crud.get_all_by_user_id",
        _fake_get_all_by_user_id,
    )

    authenticated_client(user)

    r = await async_client.get("/api/v1/users/me/registation_requests?skip=0&limit=10")
    assert r.status_code == 200
    data = r.json()["data"]
    assert data[0]["announcement_id"] == 5
    assert called["user_id"] == user.id


@pytest.mark.asyncio
async def test_get_user_organized_announcements(
    async_client, create_user, announcement_factory, monkeypatch
):
    target = await create_user(email="target@example.com", password="secret")

    datetime.now(timezone.utc).isoformat()

    fake_announcements = [
        announcement_factory.build(
            id=7, title="Target Ann", content="xx", game_id=77, organizer_id=target.id
        )
    ]

    called = {}

    async def _fake_get_all_by_organizer_id(session, organizer_id, skip=0, limit=10):
        called["organizer_id"] = organizer_id
        called["skip"] = skip
        called["limit"] = limit
        return fake_announcements

    monkeypatch.setattr(
        "api.v1.users.announcement_crud.get_all_by_organizer_id",
        _fake_get_all_by_organizer_id,
    )

    r = await async_client.get(
        f"/api/v1/users/{target.id}/organized_announcements?skip=0&limit=10"
    )
    assert r.status_code == 200
    data = r.json()["data"]
    assert data[0]["title"] == "Target Ann"
    assert called["organizer_id"] == target.id
