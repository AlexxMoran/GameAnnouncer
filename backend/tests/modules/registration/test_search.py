from datetime import datetime, timedelta

import pytest

from enums import AnnouncementFormat, SeedMethod
from enums.registration_status import RegistrationStatus
from modules.announcements.model import Announcement
from modules.games.model import Game
from modules.registration.models import RegistrationRequest
from modules.registration.schemas import RegistrationRequestFilter
from modules.registration.search import RegistrationRequestSearch


def _make_announcement(
    game_id: int, organizer_id: int, title: str = "Ann"
) -> Announcement:
    now = datetime.now()
    return Announcement(
        title=title,
        content="c",
        game_id=game_id,
        organizer_id=organizer_id,
        start_at=now + timedelta(days=30),
        registration_start_at=now,
        registration_end_at=now + timedelta(days=29),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )


@pytest.mark.asyncio
async def test_registration_request_search_filters_by_native_enum_status(
    db_session, create_user
):
    organizer = await create_user(email="rr_search_owner@example.com", password="x")
    approved_user = await create_user(
        email="rr_search_approved@example.com", password="x"
    )
    pending_user = await create_user(
        email="rr_search_pending@example.com", password="x"
    )

    game = Game(name="RRSearchGame", category="RTS", description="d")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    announcement = _make_announcement(game.id, organizer.id)
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    approved_request = RegistrationRequest(
        announcement_id=announcement.id,
        user_id=approved_user.id,
        status=RegistrationStatus.APPROVED,
    )
    pending_request = RegistrationRequest(
        announcement_id=announcement.id,
        user_id=pending_user.id,
        status=RegistrationStatus.PENDING,
    )
    db_session.add_all([approved_request, pending_request])
    await db_session.commit()

    search = RegistrationRequestSearch(
        session=db_session,
        filters=RegistrationRequestFilter(status=RegistrationStatus.PENDING),
        scope=announcement,
    )

    results = await search.results()
    count = await search.filtered_count()

    assert count == 1
    assert len(results) == 1
    assert results[0].status == RegistrationStatus.PENDING
    assert results[0].user_id == pending_user.id
