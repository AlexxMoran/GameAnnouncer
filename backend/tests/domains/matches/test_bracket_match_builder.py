import pytest
from sqlalchemy import select

from domains.matches.model import Match
from domains.matches.repository import MatchRepository
from domains.matches.services.bracket_match_builder import BracketMatchBuilder
from domains.participants.model import AnnouncementParticipant
from enums import AnnouncementStatus, MatchStatus


async def _run(
    db_session,
    announcement_id: int,
    eligible: list[AnnouncementParticipant],
    bracket_size: int,
    seeding_slots: list[int],
    third_place_match: bool = False,
) -> list[Match]:
    """Build matches and return them ordered by round and match number."""
    builder = BracketMatchBuilder(
        announcement_id=announcement_id,
        third_place_match=third_place_match,
    )
    match_repo = MatchRepository(db_session)
    await builder.call(eligible, bracket_size, seeding_slots, match_repo)
    await db_session.flush()

    result = await db_session.execute(
        select(Match)
        .where(Match.announcement_id == announcement_id)
        .order_by(Match.round_number, Match.match_number)
    )
    return list(result.scalars().all())


@pytest.mark.asyncio
async def test_full_bracket_4_participants_creates_3_matches(
    db_session, create_announcement, create_user, create_participant
):
    """4 participants, bracket_size=4 → 2 R1 matches + 1 final = 3 matches total."""
    organizer = await create_user(email="bmb_org1@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    participants = []
    for i in range(1, 5):
        user = await create_user(email=f"bmb_u1_{i}@example.com")
        p = await create_participant(announcement_id=announcement.id, user_id=user.id)
        p.seed = i
        participants.append(p)

    matches = await _run(
        db_session,
        announcement_id=announcement.id,
        eligible=participants,
        bracket_size=4,
        seeding_slots=[1, 4, 2, 3],
    )

    assert len(matches) == 3
    round_1 = [m for m in matches if m.round_number == 1]
    round_2 = [m for m in matches if m.round_number == 2]
    assert len(round_1) == 2
    assert len(round_2) == 1


@pytest.mark.asyncio
async def test_full_bracket_8_participants_creates_7_matches(
    db_session, create_announcement, create_user, create_participant
):
    """8 participants, bracket_size=8 → 4 R1 + 2 R2 + 1 Final = 7 matches."""
    organizer = await create_user(email="bmb_org2@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    participants = []
    for i in range(1, 9):
        user = await create_user(email=f"bmb_u2_{i}@example.com")
        p = await create_participant(announcement_id=announcement.id, user_id=user.id)
        p.seed = i
        participants.append(p)

    matches = await _run(
        db_session,
        announcement_id=announcement.id,
        eligible=participants,
        bracket_size=8,
        seeding_slots=[1, 8, 4, 5, 2, 7, 3, 6],
    )

    assert len(matches) == 7


@pytest.mark.asyncio
async def test_missing_seed_produces_bye_match(
    db_session, create_announcement, create_user, create_participant
):
    """3 participants in a bracket of 4 → slot for seed 4 is empty → BYE match."""
    organizer = await create_user(email="bmb_org3@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    participants = []
    for i in range(1, 4):
        user = await create_user(email=f"bmb_u3_{i}@example.com")
        p = await create_participant(announcement_id=announcement.id, user_id=user.id)
        p.seed = i
        participants.append(p)

    matches = await _run(
        db_session,
        announcement_id=announcement.id,
        eligible=participants,
        bracket_size=4,
        seeding_slots=[1, 4, 2, 3],
    )

    round_1 = sorted(
        [m for m in matches if m.round_number == 1], key=lambda m: m.match_number
    )
    assert round_1[0].is_bye is True
    assert round_1[0].winner_id == participants[0].id
    assert round_1[1].is_bye is False
    assert round_1[1].status == MatchStatus.PENDING


@pytest.mark.asyncio
async def test_bye_winner_propagated_to_round_2(
    db_session, create_announcement, create_user, create_participant
):
    """BYE winner in R1 match 1 (odd) → fills participant1_id of R2 match 1."""
    organizer = await create_user(email="bmb_org4@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    participants = []
    for i in range(1, 4):
        user = await create_user(email=f"bmb_u4_{i}@example.com")
        p = await create_participant(announcement_id=announcement.id, user_id=user.id)
        p.seed = i
        participants.append(p)

    matches = await _run(
        db_session,
        announcement_id=announcement.id,
        eligible=participants,
        bracket_size=4,
        seeding_slots=[1, 4, 2, 3],
    )

    final = next(m for m in matches if m.round_number == 2)
    assert final.participant1_id == participants[0].id


@pytest.mark.asyncio
async def test_two_byes_make_round_2_match_ready(
    db_session, create_announcement, create_user, create_participant
):
    """2 participants in bracket_size=4 → both R1 matches are BYEs → R2 match status READY."""
    organizer = await create_user(email="bmb_org5@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    p1_user = await create_user(email="bmb_u5_1@example.com")
    p2_user = await create_user(email="bmb_u5_2@example.com")
    p1 = await create_participant(announcement_id=announcement.id, user_id=p1_user.id)
    p2 = await create_participant(announcement_id=announcement.id, user_id=p2_user.id)
    p1.seed = 1
    p2.seed = 2

    matches = await _run(
        db_session,
        announcement_id=announcement.id,
        eligible=[p1, p2],
        bracket_size=4,
        seeding_slots=[1, 4, 2, 3],
    )

    final = next(m for m in matches if m.round_number == 2)
    assert final.status == MatchStatus.READY
    assert final.participant1_id == p1.id
    assert final.participant2_id == p2.id


@pytest.mark.asyncio
async def test_matches_linked_to_next_round(
    db_session, create_announcement, create_user, create_participant
):
    """R1 matches have next_match_winner_id pointing to the correct R2 match."""
    organizer = await create_user(email="bmb_org6@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    participants = []
    for i in range(1, 5):
        user = await create_user(email=f"bmb_u6_{i}@example.com")
        p = await create_participant(announcement_id=announcement.id, user_id=user.id)
        p.seed = i
        participants.append(p)

    matches = await _run(
        db_session,
        announcement_id=announcement.id,
        eligible=participants,
        bracket_size=4,
        seeding_slots=[1, 4, 2, 3],
    )

    final = next(m for m in matches if m.round_number == 2 and m.match_number == 1)
    round_1 = sorted(
        [m for m in matches if m.round_number == 1], key=lambda m: m.match_number
    )

    assert round_1[0].next_match_winner_id == final.id
    assert round_1[1].next_match_winner_id == final.id


@pytest.mark.asyncio
async def test_third_place_match_added_at_semifinal_round(
    db_session, create_announcement, create_user, create_participant
):
    """bracket_size=8 with third_place_match=True → match 3 at semifinal round (R2)."""
    organizer = await create_user(email="bmb_org7@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    participants = []
    for i in range(1, 9):
        user = await create_user(email=f"bmb_u7_{i}@example.com")
        p = await create_participant(announcement_id=announcement.id, user_id=user.id)
        p.seed = i
        participants.append(p)

    matches = await _run(
        db_session,
        announcement_id=announcement.id,
        eligible=participants,
        bracket_size=8,
        seeding_slots=[1, 8, 4, 5, 2, 7, 3, 6],
        third_place_match=True,
    )

    third_place = next((m for m in matches if m.is_third_place), None)
    assert third_place is not None
    assert third_place.round_number == 2
    assert third_place.match_number == 3
    assert third_place.status == MatchStatus.PENDING


@pytest.mark.asyncio
async def test_no_third_place_match_when_disabled(
    db_session, create_announcement, create_user, create_participant
):
    """third_place_match=False → no match with is_third_place=True created."""
    organizer = await create_user(email="bmb_org8@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    participants = []
    for i in range(1, 9):
        user = await create_user(email=f"bmb_u8_{i}@example.com")
        p = await create_participant(announcement_id=announcement.id, user_id=user.id)
        p.seed = i
        participants.append(p)

    matches = await _run(
        db_session,
        announcement_id=announcement.id,
        eligible=participants,
        bracket_size=8,
        seeding_slots=[1, 8, 4, 5, 2, 7, 3, 6],
        third_place_match=False,
    )

    assert all(not m.is_third_place for m in matches)
    assert len(matches) == 7
