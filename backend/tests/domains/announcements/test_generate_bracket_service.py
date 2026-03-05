import math

import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domains.announcements.model import Announcement
from domains.announcements.services.generate_bracket import GenerateBracketService
from domains.matches.model import Match
from enums import AnnouncementStatus, MatchStatus
from exceptions import ValidationException


async def _reload(db_session, announcement_id: int) -> Announcement:
    """Reload announcement with participants eagerly loaded.

    Uses populate_existing=True to bypass the session identity map so that
    freshly created participants are reflected on the returned object.
    """
    result = await db_session.execute(
        select(Announcement)
        .options(selectinload(Announcement.participants))
        .where(Announcement.id == announcement_id)
        .execution_options(populate_existing=True)
    )
    return result.scalar_one()


async def _get_matches(db_session, announcement_id: int) -> list[Match]:
    """Fetch all matches for an announcement ordered by round and match number."""
    result = await db_session.execute(
        select(Match)
        .where(Match.announcement_id == announcement_id)
        .order_by(Match.round_number, Match.match_number)
    )
    return list(result.scalars().all())


@pytest.mark.asyncio
async def test_bracket_generated_for_non_qual_announcement(
    db_session, create_user, create_announcement, create_participant
):
    """8 participants with no qualification → 7 matches (4 R1 + 2 R2 + 1 Final), no third-place."""
    organizer = await create_user(email="gb_org1@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=False,
        third_place_match=False,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    for i in range(1, 9):
        user = await create_user(email=f"gb_u1_{i}@example.com")
        await create_participant(announcement_id=announcement.id, user_id=user.id)

    announcement = await _reload(db_session, announcement.id)
    await GenerateBracketService(announcement, db_session, organizer).call()
    await db_session.commit()

    matches = await _get_matches(db_session, announcement.id)
    assert len(matches) == 7

    by_round = {}
    for match in matches:
        by_round.setdefault(match.round_number, []).append(match)

    assert len(by_round[1]) == 4
    assert len(by_round[2]) == 2
    assert len(by_round[3]) == 1


@pytest.mark.asyncio
async def test_bracket_generated_after_qualification(
    db_session, create_user, create_announcement, create_participant
):
    """5 participants → 4 qualified → bracket_size=4 → 3 matches (2 R1 + 1 Final), no third-place."""
    organizer = await create_user(email="gb_org2@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=True,
        qualification_finished=True,
        bracket_size=4,
        third_place_match=False,
        status=AnnouncementStatus.LIVE,
    )
    for i, score in enumerate([90, 80, 70, 60], start=1):
        user = await create_user(email=f"gb_u2_{i}@example.com")
        await create_participant(
            announcement_id=announcement.id,
            user_id=user.id,
            qualification_score=score,
            qualification_rank=i,
            is_qualified=True,
        )
    cutoff_user = await create_user(email="gb_u2_5@example.com")
    await create_participant(
        announcement_id=announcement.id,
        user_id=cutoff_user.id,
        qualification_score=50,
        qualification_rank=5,
        is_qualified=False,
    )

    announcement = await _reload(db_session, announcement.id)
    await GenerateBracketService(announcement, db_session, organizer).call()
    await db_session.commit()

    matches = await _get_matches(db_session, announcement.id)
    assert len(matches) == 3


@pytest.mark.asyncio
async def test_seeds_assigned_correctly(
    db_session, create_user, create_announcement, create_participant
):
    """Seeds 1..N are assigned to participants in registration order."""
    organizer = await create_user(email="gb_org3@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=False,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    participants = []
    for i in range(1, 5):
        user = await create_user(email=f"gb_u3_{i}@example.com")
        participant = await create_participant(
            announcement_id=announcement.id, user_id=user.id
        )
        participants.append(participant)

    announcement = await _reload(db_session, announcement.id)
    await GenerateBracketService(announcement, db_session, organizer).call()
    await db_session.commit()

    for participant in participants:
        await db_session.refresh(participant)

    assigned_seeds = sorted(p.seed for p in participants)
    assert assigned_seeds == [1, 2, 3, 4]


@pytest.mark.asyncio
async def test_standard_seeding_order_r1(
    db_session, create_user, create_announcement, create_participant
):
    """In an 8-team bracket: R1 matchups follow standard seeding: 1v8, 4v5, 2v7, 3v6."""
    organizer = await create_user(email="gb_org4@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=False,
        third_place_match=False,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    participants = []
    for i in range(1, 9):
        user = await create_user(email=f"gb_u4_{i}@example.com")
        participant = await create_participant(
            announcement_id=announcement.id, user_id=user.id
        )
        participants.append(participant)

    announcement = await _reload(db_session, announcement.id)
    await GenerateBracketService(announcement, db_session, organizer).call()
    await db_session.commit()

    for participant in participants:
        await db_session.refresh(participant)

    seed_to_participant = {p.seed: p for p in participants}

    matches = await _get_matches(db_session, announcement.id)
    round_1_matches = sorted(
        [m for m in matches if m.round_number == 1], key=lambda m: m.match_number
    )

    expected_pairs = [(1, 8), (4, 5), (2, 7), (3, 6)]
    for match, (top_seed, bottom_seed) in zip(round_1_matches, expected_pairs):
        assert match.participant1_id == seed_to_participant[top_seed].id
        assert match.participant2_id == seed_to_participant[bottom_seed].id


@pytest.mark.asyncio
async def test_bye_match_has_correct_winner(
    db_session, create_user, create_announcement, create_participant
):
    """6 participants in bracket of 8 → 2 BYE matches with winner_id set to the existing participant."""
    organizer = await create_user(email="gb_org5@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=False,
        third_place_match=False,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    for i in range(1, 7):
        user = await create_user(email=f"gb_u5_{i}@example.com")
        await create_participant(announcement_id=announcement.id, user_id=user.id)

    announcement = await _reload(db_session, announcement.id)
    await GenerateBracketService(announcement, db_session, organizer).call()
    await db_session.commit()

    matches = await _get_matches(db_session, announcement.id)
    bye_matches = [m for m in matches if m.is_bye]

    assert len(bye_matches) == 2
    for bye_match in bye_matches:
        assert bye_match.winner_id is not None
        assert bye_match.status == MatchStatus.BYE
        assert bye_match.winner_id in (
            bye_match.participant1_id,
            bye_match.participant2_id,
        )


@pytest.mark.asyncio
async def test_bye_winner_propagated_to_r2(
    db_session, create_user, create_announcement, create_participant
):
    """BYE winners in R1 are immediately set as participants in the corresponding R2 match."""
    organizer = await create_user(email="gb_org6@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=False,
        third_place_match=False,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    for i in range(1, 4):
        user = await create_user(email=f"gb_u6_{i}@example.com")
        await create_participant(announcement_id=announcement.id, user_id=user.id)

    announcement = await _reload(db_session, announcement.id)
    await GenerateBracketService(announcement, db_session, organizer).call()
    await db_session.commit()

    matches = await _get_matches(db_session, announcement.id)
    round_1_matches = [m for m in matches if m.round_number == 1]
    round_2_matches = [m for m in matches if m.round_number == 2]

    bye_matches = [m for m in round_1_matches if m.is_bye]
    assert len(bye_matches) == 1

    for bye_match in bye_matches:
        next_match_number = math.ceil(bye_match.match_number / 2)
        next_match = next(
            (m for m in round_2_matches if m.match_number == next_match_number), None
        )
        assert next_match is not None
        if bye_match.match_number % 2 == 1:
            assert next_match.participant1_id == bye_match.winner_id
        else:
            assert next_match.participant2_id == bye_match.winner_id


@pytest.mark.asyncio
async def test_third_place_match_created(
    db_session, create_user, create_announcement, create_participant
):
    """When third_place_match=True and bracket_size>=4, a match with is_third_place=True is created."""
    organizer = await create_user(email="gb_org7@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=False,
        third_place_match=True,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    for i in range(1, 5):
        user = await create_user(email=f"gb_u7_{i}@example.com")
        await create_participant(announcement_id=announcement.id, user_id=user.id)

    announcement = await _reload(db_session, announcement.id)
    await GenerateBracketService(announcement, db_session, organizer).call()
    await db_session.commit()

    matches = await _get_matches(db_session, announcement.id)
    third_place_matches = [m for m in matches if m.is_third_place]
    assert len(third_place_matches) == 1

    num_rounds = int(math.log2(4))
    semifinal_round = num_rounds - 1
    assert third_place_matches[0].round_number == semifinal_round
    assert third_place_matches[0].match_number == 3


@pytest.mark.asyncio
async def test_next_match_winner_id_linked(
    db_session, create_user, create_announcement, create_participant
):
    """R1.M1 and R1.M2 both link their next_match_winner_id to R2.M1."""
    organizer = await create_user(email="gb_org8@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=False,
        third_place_match=False,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    for i in range(1, 5):
        user = await create_user(email=f"gb_u8_{i}@example.com")
        await create_participant(announcement_id=announcement.id, user_id=user.id)

    announcement = await _reload(db_session, announcement.id)
    await GenerateBracketService(announcement, db_session, organizer).call()
    await db_session.commit()

    matches = await _get_matches(db_session, announcement.id)
    round_1_matches = sorted(
        [m for m in matches if m.round_number == 1], key=lambda m: m.match_number
    )
    round_2_match_1 = next(
        m for m in matches if m.round_number == 2 and m.match_number == 1
    )

    assert round_1_matches[0].next_match_winner_id == round_2_match_1.id
    assert round_1_matches[1].next_match_winner_id == round_2_match_1.id


@pytest.mark.asyncio
async def test_raises_when_qual_not_finished(
    db_session, create_user, create_announcement, create_participant
):
    """ValidationException when has_qualification=True but qualification_finished=False."""
    organizer = await create_user(email="gb_org9@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=True,
        qualification_finished=False,
        status=AnnouncementStatus.LIVE,
    )
    user = await create_user(email="gb_u9@example.com")
    await create_participant(announcement_id=announcement.id, user_id=user.id)

    announcement = await _reload(db_session, announcement.id)
    with pytest.raises(ValidationException, match="Qualification must be finalized"):
        await GenerateBracketService(announcement, db_session, organizer).call()


@pytest.mark.asyncio
async def test_raises_when_bracket_already_generated(
    db_session, create_user, create_announcement, create_participant, create_match
):
    """ValidationException when matches already exist for the announcement."""
    organizer = await create_user(email="gb_org10@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=False,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    await create_match(
        announcement_id=announcement.id,
        round_number=1,
        match_number=1,
    )

    announcement = await _reload(db_session, announcement.id)
    with pytest.raises(ValidationException, match="already been generated"):
        await GenerateBracketService(announcement, db_session, organizer).call()


@pytest.mark.asyncio
async def test_raises_when_no_eligible_participants(
    db_session, create_user, create_announcement
):
    """ValidationException when there are no eligible participants."""
    organizer = await create_user(email="gb_org11@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=False,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )

    announcement = await _reload(db_session, announcement.id)
    with pytest.raises(ValidationException, match="At least 2 eligible participants"):
        await GenerateBracketService(announcement, db_session, organizer).call()


@pytest.mark.asyncio
async def test_bracket_size_set_on_announcement_for_non_qual(
    db_session, create_user, create_announcement, create_participant
):
    """announcement.bracket_size is computed and persisted for non-qualification announcements."""
    organizer = await create_user(email="gb_org12@example.com")
    announcement = await create_announcement(
        organizer_id=organizer.id,
        has_qualification=False,
        status=AnnouncementStatus.REGISTRATION_CLOSED,
    )
    for i in range(1, 7):
        user = await create_user(email=f"gb_u12_{i}@example.com")
        await create_participant(announcement_id=announcement.id, user_id=user.id)

    announcement = await _reload(db_session, announcement.id)
    result = await GenerateBracketService(announcement, db_session, organizer).call()
    await db_session.commit()

    assert result.bracket_size == 8
