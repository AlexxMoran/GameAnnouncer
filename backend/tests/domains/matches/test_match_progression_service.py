import pytest
from sqlalchemy import select

from domains.matches.model import Match
from domains.matches.schemas import MatchResultUpdate
from domains.matches.services.match_progression import MatchProgressionService
from enums import AnnouncementStatus, MatchStatus
from exceptions import ValidationException


async def _reload_match(db_session, match_id: int) -> Match:
    """Reload a match from the DB, bypassing the session identity map."""
    result = await db_session.execute(
        select(Match)
        .where(Match.id == match_id)
        .execution_options(populate_existing=True)
    )
    return result.scalar_one()


@pytest.mark.asyncio
async def test_winner_is_set_and_match_completed(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """Reporting a result marks the match COMPLETED and sets winner_id."""
    organizer = await create_user(email="mp_org1@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id, status=AnnouncementStatus.LIVE
    )
    u1 = await create_user(email="mp_u1a@example.com")
    u2 = await create_user(email="mp_u1b@example.com")
    p1 = await create_participant(announcement_id=announcement.id, user_id=u1.id)
    p2 = await create_participant(announcement_id=announcement.id, user_id=u2.id)

    final = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        status=MatchStatus.READY,
        participant1_id=p1.id,
        participant2_id=p2.id,
    )

    body = MatchResultUpdate(winner="participant1")
    await MatchProgressionService(final, announcement, body, db_session).call()
    await db_session.commit()

    final = await _reload_match(db_session, final.id)
    assert final.winner_id == p1.id
    assert final.status == MatchStatus.COMPLETED


@pytest.mark.asyncio
async def test_winner_advances_to_next_match_odd_slot(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """Odd match_number winner goes into participant1_id of the next match."""
    organizer = await create_user(email="mp_org2@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id, status=AnnouncementStatus.LIVE
    )
    u1 = await create_user(email="mp_u2a@example.com")
    u2 = await create_user(email="mp_u2b@example.com")
    u3 = await create_user(email="mp_u2c@example.com")
    p1 = await create_participant(announcement_id=announcement.id, user_id=u1.id)
    p2 = await create_participant(announcement_id=announcement.id, user_id=u2.id)
    p3 = await create_participant(announcement_id=announcement.id, user_id=u3.id)

    final = await create_match(
        announcement_id=announcement.id,
        round_number=2,
        match_number=1,
        status=MatchStatus.PENDING,
        participant1_id=None,
        participant2_id=p3.id,
    )
    semi = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        status=MatchStatus.READY,
        participant1_id=p1.id,
        participant2_id=p2.id,
        next_match_winner_id=final.id,
    )

    body = MatchResultUpdate(winner="participant1")
    await MatchProgressionService(semi, announcement, body, db_session).call()
    await db_session.commit()

    final = await _reload_match(db_session, final.id)
    assert final.participant1_id == p1.id


@pytest.mark.asyncio
async def test_winner_advances_to_next_match_even_slot(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """Even match_number winner goes into participant2_id of the next match."""
    organizer = await create_user(email="mp_org3@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id, status=AnnouncementStatus.LIVE
    )
    u1 = await create_user(email="mp_u3a@example.com")
    u2 = await create_user(email="mp_u3b@example.com")
    u3 = await create_user(email="mp_u3c@example.com")
    p1 = await create_participant(announcement_id=announcement.id, user_id=u1.id)
    p2 = await create_participant(announcement_id=announcement.id, user_id=u2.id)
    p3 = await create_participant(announcement_id=announcement.id, user_id=u3.id)

    final = await create_match(
        announcement_id=announcement.id,
        round_number=2,
        match_number=1,
        status=MatchStatus.PENDING,
        participant1_id=p3.id,
        participant2_id=None,
    )
    semi = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=2,
        status=MatchStatus.READY,
        participant1_id=p1.id,
        participant2_id=p2.id,
        next_match_winner_id=final.id,
    )

    body = MatchResultUpdate(winner="participant2")
    await MatchProgressionService(semi, announcement, body, db_session).call()
    await db_session.commit()

    final = await _reload_match(db_session, final.id)
    assert final.participant2_id == p2.id


@pytest.mark.asyncio
async def test_next_match_becomes_ready_when_both_slots_filled(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """Next match status becomes READY once both participant slots are filled."""
    organizer = await create_user(email="mp_org4@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id, status=AnnouncementStatus.LIVE
    )
    u1 = await create_user(email="mp_u4a@example.com")
    u2 = await create_user(email="mp_u4b@example.com")
    u3 = await create_user(email="mp_u4c@example.com")
    p1 = await create_participant(announcement_id=announcement.id, user_id=u1.id)
    p2 = await create_participant(announcement_id=announcement.id, user_id=u2.id)
    p3 = await create_participant(announcement_id=announcement.id, user_id=u3.id)

    final = await create_match(
        announcement_id=announcement.id,
        round_number=2,
        match_number=1,
        status=MatchStatus.PENDING,
        participant1_id=p3.id,
        participant2_id=None,
    )
    semi = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=2,
        status=MatchStatus.READY,
        participant1_id=p1.id,
        participant2_id=p2.id,
        next_match_winner_id=final.id,
    )

    body = MatchResultUpdate(winner="participant1")
    await MatchProgressionService(semi, announcement, body, db_session).call()
    await db_session.commit()

    final = await _reload_match(db_session, final.id)
    assert final.status == MatchStatus.READY


@pytest.mark.asyncio
async def test_semifinal_loser_fills_third_place_odd_slot(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """Odd-numbered semifinal loser goes into participant1_id of the third-place match."""
    organizer = await create_user(email="mp_org5@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        status=AnnouncementStatus.LIVE,
        third_place_match=True,
    )
    u1 = await create_user(email="mp_u5a@example.com")
    u2 = await create_user(email="mp_u5b@example.com")
    u3 = await create_user(email="mp_u5c@example.com")
    p1 = await create_participant(announcement_id=announcement.id, user_id=u1.id)
    p2 = await create_participant(announcement_id=announcement.id, user_id=u2.id)
    p3 = await create_participant(announcement_id=announcement.id, user_id=u3.id)

    final = await create_match(
        announcement_id=announcement.id,
        round_number=2,
        match_number=1,
        status=MatchStatus.PENDING,
        participant1_id=None,
        participant2_id=p3.id,
    )
    third_place = await create_match(
        announcement_id=announcement.id,
        round_number=2,
        match_number=3,
        status=MatchStatus.PENDING,
        is_third_place=True,
        participant1_id=None,
        participant2_id=None,
    )
    semi = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        status=MatchStatus.READY,
        participant1_id=p1.id,
        participant2_id=p2.id,
        next_match_winner_id=final.id,
    )

    body = MatchResultUpdate(winner="participant1")
    await MatchProgressionService(semi, announcement, body, db_session).call()
    await db_session.commit()

    third_place = await _reload_match(db_session, third_place.id)
    assert third_place.participant1_id == p2.id


@pytest.mark.asyncio
async def test_third_place_match_becomes_ready_after_both_semis(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """Third-place match becomes READY after both semifinals report losers."""
    organizer = await create_user(email="mp_org6@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        status=AnnouncementStatus.LIVE,
        third_place_match=True,
    )
    users = [await create_user(email=f"mp_u6_{i}@example.com") for i in range(4)]
    ps = [
        await create_participant(announcement_id=announcement.id, user_id=u.id)
        for u in users
    ]

    final = await create_match(
        announcement_id=announcement.id,
        round_number=2,
        match_number=1,
        status=MatchStatus.PENDING,
        participant1_id=None,
        participant2_id=None,
    )
    third_place = await create_match(
        announcement_id=announcement.id,
        round_number=2,
        match_number=3,
        status=MatchStatus.PENDING,
        is_third_place=True,
        participant1_id=None,
        participant2_id=None,
    )
    semi1 = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        status=MatchStatus.READY,
        participant1_id=ps[0].id,
        participant2_id=ps[1].id,
        next_match_winner_id=final.id,
    )
    semi2 = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=2,
        status=MatchStatus.READY,
        participant1_id=ps[2].id,
        participant2_id=ps[3].id,
        next_match_winner_id=final.id,
    )

    body1 = MatchResultUpdate(winner="participant1")
    await MatchProgressionService(semi1, announcement, body1, db_session).call()
    await db_session.flush()

    semi2 = await _reload_match(db_session, semi2.id)
    body2 = MatchResultUpdate(winner="participant1")
    await MatchProgressionService(semi2, announcement, body2, db_session).call()
    await db_session.commit()

    third_place = await _reload_match(db_session, third_place.id)
    assert third_place.participant1_id == ps[1].id
    assert third_place.participant2_id == ps[3].id
    assert third_place.status == MatchStatus.READY


@pytest.mark.asyncio
async def test_final_assigns_placements_1_and_2(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """Winner of the final gets placement=1, loser gets placement=2."""
    organizer = await create_user(email="mp_org7@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id, status=AnnouncementStatus.LIVE
    )
    u1 = await create_user(email="mp_u7a@example.com")
    u2 = await create_user(email="mp_u7b@example.com")
    p1 = await create_participant(announcement_id=announcement.id, user_id=u1.id)
    p2 = await create_participant(announcement_id=announcement.id, user_id=u2.id)

    final = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        status=MatchStatus.READY,
        participant1_id=p1.id,
        participant2_id=p2.id,
    )

    body = MatchResultUpdate(winner="participant1")
    await MatchProgressionService(final, announcement, body, db_session).call()
    await db_session.commit()

    await db_session.refresh(p1)
    await db_session.refresh(p2)
    assert p1.placement == 1
    assert p2.placement == 2


@pytest.mark.asyncio
async def test_third_place_match_assigns_placements_3_and_4(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """Winner of the third-place match gets placement=3, loser gets placement=4."""
    organizer = await create_user(email="mp_org8@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id, status=AnnouncementStatus.LIVE
    )
    u1 = await create_user(email="mp_u8a@example.com")
    u2 = await create_user(email="mp_u8b@example.com")
    p1 = await create_participant(announcement_id=announcement.id, user_id=u1.id)
    p2 = await create_participant(announcement_id=announcement.id, user_id=u2.id)

    third_place = await create_match(
        announcement_id=announcement.id,
        round_number=2,
        match_number=3,
        status=MatchStatus.READY,
        is_third_place=True,
        participant1_id=p1.id,
        participant2_id=p2.id,
    )

    await create_match(
        announcement_id=announcement.id,
        round_number=2,
        match_number=1,
        status=MatchStatus.COMPLETED,
        participant1_id=None,
        participant2_id=None,
    )

    body = MatchResultUpdate(winner="participant2")
    await MatchProgressionService(third_place, announcement, body, db_session).call()
    await db_session.commit()

    await db_session.refresh(p1)
    await db_session.refresh(p2)
    assert p2.placement == 3
    assert p1.placement == 4


@pytest.mark.asyncio
async def test_tournament_completes_and_announcement_becomes_finished(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """After the only match completes, announcement transitions to FINISHED."""
    organizer = await create_user(email="mp_org9@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id, status=AnnouncementStatus.LIVE
    )
    u1 = await create_user(email="mp_u9a@example.com")
    u2 = await create_user(email="mp_u9b@example.com")
    p1 = await create_participant(announcement_id=announcement.id, user_id=u1.id)
    p2 = await create_participant(announcement_id=announcement.id, user_id=u2.id)

    final = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        status=MatchStatus.READY,
        participant1_id=p1.id,
        participant2_id=p2.id,
    )

    body = MatchResultUpdate(winner="participant1")
    await MatchProgressionService(final, announcement, body, db_session).call()
    await db_session.commit()

    await db_session.refresh(announcement)
    assert announcement.status == AnnouncementStatus.FINISHED


@pytest.mark.asyncio
async def test_raises_when_match_not_ready(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """ValidationException when trying to report a result on a PENDING match."""
    organizer = await create_user(email="mp_org10@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id, status=AnnouncementStatus.LIVE
    )
    u1 = await create_user(email="mp_u10a@example.com")
    u2 = await create_user(email="mp_u10b@example.com")
    p1 = await create_participant(announcement_id=announcement.id, user_id=u1.id)
    p2 = await create_participant(announcement_id=announcement.id, user_id=u2.id)

    match = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        status=MatchStatus.PENDING,
        participant1_id=p1.id,
        participant2_id=p2.id,
    )

    with pytest.raises(ValidationException, match="not ready"):
        await MatchProgressionService(
            match,
            announcement,
            MatchResultUpdate(winner="participant1"),
            db_session,
        ).call()


@pytest.mark.asyncio
async def test_raises_when_match_is_bye(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """ValidationException when trying to report a result on a BYE match."""
    organizer = await create_user(email="mp_org12@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id, status=AnnouncementStatus.LIVE
    )
    u1 = await create_user(email="mp_u12a@example.com")
    p1 = await create_participant(announcement_id=announcement.id, user_id=u1.id)

    bye_match = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        status=MatchStatus.READY,
        is_bye=True,
        participant1_id=p1.id,
        participant2_id=None,
    )

    with pytest.raises(ValidationException, match="BYE"):
        await MatchProgressionService(
            bye_match,
            announcement,
            MatchResultUpdate(winner="participant1"),
            db_session,
        ).call()


@pytest.mark.asyncio
async def test_raises_when_selected_winner_slot_is_empty(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """ValidationException when selected winner slot has no participant."""
    organizer = await create_user(email="mp_org13@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id, status=AnnouncementStatus.LIVE
    )
    u1 = await create_user(email="mp_u13a@example.com")
    p1 = await create_participant(announcement_id=announcement.id, user_id=u1.id)

    match = await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
        status=MatchStatus.READY,
        participant1_id=p1.id,
        participant2_id=None,
    )

    with pytest.raises(ValidationException, match="winner slot is empty"):
        await MatchProgressionService(
            match,
            announcement,
            MatchResultUpdate(winner="participant2"),
            db_session,
        ).call()
