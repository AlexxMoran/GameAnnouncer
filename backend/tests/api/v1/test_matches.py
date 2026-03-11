import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from enums import MatchStatus
from exceptions import AppException


def _make_match(
    match_id: int = 1,
    announcement_id: int = 10,
    round_number: int = 1,
    match_number: int = 1,
    status: MatchStatus = MatchStatus.READY,
    participant1_id: int | None = 2,
    participant2_id: int | None = 3,
    winner_id: int | None = None,
    is_bye: bool = False,
    is_third_place: bool = False,
    next_match_winner_id: int | None = None,
) -> SimpleNamespace:
    """Build a lightweight match-like object for use in API tests."""
    return SimpleNamespace(
        id=match_id,
        announcement_id=announcement_id,
        round_number=round_number,
        match_number=match_number,
        status=status,
        participant1_id=participant1_id,
        participant2_id=participant2_id,
        participant1=None,
        participant2=None,
        winner_id=winner_id,
        is_bye=is_bye,
        is_third_place=is_third_place,
        next_match_winner_id=next_match_winner_id,
        completed_at=None,
    )


@pytest.mark.asyncio
async def test_get_match_returns_200(async_client):
    match = _make_match()

    with patch(
        "api.v1.matches.MatchRepository.find_by_id",
        new=AsyncMock(return_value=match),
    ):
        r = await async_client.get("/api/v1/matches/1")
        assert r.status_code == 200
        body = r.json()
        assert body["data"]["id"] == 1
        assert body["data"]["status"] == MatchStatus.READY.value


@pytest.mark.asyncio
async def test_get_match_returns_404_when_not_found(async_client):
    with patch(
        "api.v1.matches.MatchRepository.find_by_id",
        new=AsyncMock(return_value=None),
    ):
        r = await async_client.get("/api/v1/matches/999")
        assert r.status_code == 404


@pytest.mark.asyncio
async def test_set_match_result_returns_200_for_organizer(
    async_client, authenticated_client, user
):
    client = authenticated_client(user)
    match = _make_match()
    completed_match = _make_match(status=MatchStatus.COMPLETED, winner_id=2)

    announcement = SimpleNamespace(
        id=10,
        organizer_id=user.id,
        status="LIVE",
        third_place_match=False,
    )

    class FakeService:
        def __init__(self, match, announcement, result_in, session):
            pass

        async def call(self):
            return completed_match

    with (
        patch("api.v1.matches.authorize_action"),
        patch(
            "api.v1.matches.MatchRepository.find_by_id",
            new=AsyncMock(return_value=match),
        ),
        patch(
            "api.v1.matches.AnnouncementRepository.find_by_id",
            new=AsyncMock(return_value=announcement),
        ),
        patch("api.v1.matches.MatchProgressionService", new=FakeService),
    ):
        r = await client.patch(
            "/api/v1/matches/1/result", json={"winner": "participant1"}
        )
        assert r.status_code == 200
        body = r.json()
        assert body["data"]["status"] == MatchStatus.COMPLETED.value
        assert body["data"]["winner_id"] == 2


@pytest.mark.asyncio
async def test_set_match_result_returns_401_for_unauthenticated(async_client):
    import core.users as users_mod

    app = async_client._transport.app
    app.dependency_overrides.pop(users_mod.current_user, None)

    match = _make_match()
    announcement = SimpleNamespace(
        id=10, organizer_id=1, status="LIVE", third_place_match=False
    )

    with (
        patch(
            "api.v1.matches.MatchRepository.find_by_id",
            new=AsyncMock(return_value=match),
        ),
        patch(
            "api.v1.matches.AnnouncementRepository.find_by_id",
            new=AsyncMock(return_value=announcement),
        ),
    ):
        r = await async_client.patch(
            "/api/v1/matches/1/result", json={"winner": "participant1"}
        )
        assert r.status_code == 401


@pytest.mark.asyncio
async def test_set_match_result_returns_403_for_non_organizer(
    async_client, authenticated_client, user
):
    client = authenticated_client(user)
    match = _make_match()

    other_organizer_id = user.id + 100
    announcement = SimpleNamespace(
        id=10,
        organizer_id=other_organizer_id,
        status="LIVE",
        third_place_match=False,
    )

    with (
        patch(
            "api.v1.matches.MatchRepository.find_by_id",
            new=AsyncMock(return_value=match),
        ),
        patch(
            "api.v1.matches.AnnouncementRepository.find_by_id",
            new=AsyncMock(return_value=announcement),
        ),
        patch(
            "api.v1.matches.authorize_action",
            side_effect=AppException("Forbidden", status_code=403),
        ),
    ):
        r = await client.patch(
            "/api/v1/matches/1/result", json={"winner": "participant1"}
        )
        assert r.status_code == 403


@pytest.mark.asyncio
async def test_set_match_result_returns_404_when_match_not_found(
    async_client, authenticated_client, user
):
    client = authenticated_client(user)

    with patch(
        "api.v1.matches.MatchRepository.find_by_id",
        new=AsyncMock(return_value=None),
    ):
        r = await client.patch(
            "/api/v1/matches/999/result", json={"winner": "participant1"}
        )
        assert r.status_code == 404
