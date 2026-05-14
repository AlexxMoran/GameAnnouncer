import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.asyncio
async def test_get_my_registration_requests_requires_auth(async_client):
    import core.users as users_mod

    app = async_client._transport.app
    popped = app.dependency_overrides.pop(users_mod.current_user, None)

    try:
        r = await async_client.get("/api/v1/users/me/registration_requests")
    finally:
        if popped is not None:
            app.dependency_overrides[users_mod.current_user] = popped

    assert r.status_code == 401


@pytest.mark.asyncio
async def test_get_my_registration_requests_uses_search_with_status_filter(
    async_client, authenticated_client, user
):
    client = authenticated_client(user)

    mock_search = MagicMock()
    mock_search.results = AsyncMock(return_value=[])
    mock_search.filtered_count = AsyncMock(return_value=0)
    mock_search.total_count = AsyncMock(return_value=3)

    with patch(
        "api.v1.users.RegistrationRequestSearch",
        return_value=mock_search,
    ) as search_cls:
        r = await client.get("/api/v1/users/me/registration_requests?status=pending")

    assert r.status_code == 200
    body = r.json()
    assert body["data"] == []
    assert body["filtered_count"] == 0
    assert body["total_count"] == 3

    search_cls.assert_called_once()
    called_kwargs = search_cls.call_args.kwargs
    assert called_kwargs["scope"].id == user.id
    assert called_kwargs["filters"].status == "pending"
