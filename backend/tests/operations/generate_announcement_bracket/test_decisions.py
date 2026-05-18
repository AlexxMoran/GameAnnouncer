from datetime import datetime, timedelta, timezone

import pytest

from enums import AnnouncementStatus
from exceptions import ValidationException
from operations.generate_announcement_bracket.decisions import (
    GenerateAnnouncementBracketDecisions,
)
from operations.generate_announcement_bracket.structures import (
    BracketParticipantSnapshot,
    GenerateAnnouncementBracketSnapshot,
)


def _participant(
    participant_id: int,
    *,
    created_at: datetime | None = None,
    is_qualified: bool = False,
    qualification_rank: int | None = None,
) -> BracketParticipantSnapshot:
    return BracketParticipantSnapshot(
        id=participant_id,
        created_at=created_at or datetime.now(timezone.utc),
        is_qualified=is_qualified,
        qualification_rank=qualification_rank,
    )


def _snapshot(
    *,
    status: AnnouncementStatus = AnnouncementStatus.REGISTRATION_CLOSED,
    has_qualification: bool = False,
    qualification_finished: bool = False,
    bracket_size: int | None = None,
    third_place_match: bool = False,
    participants: list[BracketParticipantSnapshot] | None = None,
    has_existing_matches: bool = False,
) -> GenerateAnnouncementBracketSnapshot:
    return GenerateAnnouncementBracketSnapshot(
        announcement_id=1,
        status=status,
        has_qualification=has_qualification,
        qualification_finished=qualification_finished,
        bracket_size=bracket_size,
        third_place_match=third_place_match,
        participants=participants or [],
        has_existing_matches=has_existing_matches,
    )


def test_direct_bracket_decision_assigns_seeds_by_registration_order():
    now = datetime.now(timezone.utc)
    snapshot = _snapshot(
        participants=[
            _participant(2, created_at=now + timedelta(seconds=2)),
            _participant(1, created_at=now + timedelta(seconds=1)),
            _participant(3, created_at=now + timedelta(seconds=3)),
        ]
    )

    decision = GenerateAnnouncementBracketDecisions().make(snapshot)

    assert decision.announcement_id == 1
    assert decision.bracket_size == 4
    assert decision.seeding_slots == [1, 4, 2, 3]
    assert [(s.participant_id, s.seed) for s in decision.participant_seeds] == [
        (1, 1),
        (2, 2),
        (3, 3),
    ]


def test_qualification_bracket_decision_uses_qualified_rank_order():
    snapshot = _snapshot(
        status=AnnouncementStatus.LIVE,
        has_qualification=True,
        qualification_finished=True,
        bracket_size=4,
        third_place_match=True,
        participants=[
            _participant(1, is_qualified=True, qualification_rank=2),
            _participant(2, is_qualified=False, qualification_rank=3),
            _participant(3, is_qualified=True, qualification_rank=1),
            _participant(4, is_qualified=True, qualification_rank=4),
        ],
    )

    decision = GenerateAnnouncementBracketDecisions().make(snapshot)

    assert decision.bracket_size == 4
    assert decision.third_place_match is True
    assert [(s.participant_id, s.seed) for s in decision.participant_seeds] == [
        (3, 1),
        (1, 2),
        (4, 3),
    ]


def test_decision_rejects_existing_bracket():
    snapshot = _snapshot(
        participants=[_participant(1), _participant(2)],
        has_existing_matches=True,
    )

    with pytest.raises(ValidationException, match="already been generated"):
        GenerateAnnouncementBracketDecisions().make(snapshot)


def test_decision_rejects_direct_bracket_before_registration_closed():
    snapshot = _snapshot(
        status=AnnouncementStatus.REGISTRATION_OPEN,
        participants=[_participant(1), _participant(2)],
    )

    with pytest.raises(ValidationException, match="generate_bracket"):
        GenerateAnnouncementBracketDecisions().make(snapshot)


def test_decision_rejects_unfinished_qualification():
    snapshot = _snapshot(
        status=AnnouncementStatus.LIVE,
        has_qualification=True,
        qualification_finished=False,
        bracket_size=4,
        participants=[
            _participant(1, is_qualified=True, qualification_rank=1),
            _participant(2, is_qualified=True, qualification_rank=2),
        ],
    )

    with pytest.raises(ValidationException, match="Qualification must be finalized"):
        GenerateAnnouncementBracketDecisions().make(snapshot)


def test_decision_rejects_too_few_eligible_participants():
    snapshot = _snapshot(participants=[_participant(1)])

    with pytest.raises(ValidationException, match="At least 2 eligible participants"):
        GenerateAnnouncementBracketDecisions().make(snapshot)
