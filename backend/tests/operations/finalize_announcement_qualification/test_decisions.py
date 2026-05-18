from datetime import datetime, timedelta, timezone

import pytest

from enums import AnnouncementStatus
from exceptions import ValidationException
from operations.finalize_announcement_qualification.decisions import (
    FinalizeAnnouncementQualificationDecisions,
)
from operations.finalize_announcement_qualification.structures import (
    FinalizeAnnouncementQualificationSnapshot,
    QualificationParticipantSnapshot,
)


def _participant(
    participant_id: int,
    *,
    score: int | None = None,
    created_at: datetime | None = None,
) -> QualificationParticipantSnapshot:
    return QualificationParticipantSnapshot(
        id=participant_id,
        qualification_score=score,
        created_at=created_at or datetime.now(timezone.utc),
    )


def _snapshot(
    *,
    status: AnnouncementStatus = AnnouncementStatus.LIVE,
    has_qualification: bool = True,
    qualification_finished: bool = False,
    participants: list[QualificationParticipantSnapshot] | None = None,
) -> FinalizeAnnouncementQualificationSnapshot:
    return FinalizeAnnouncementQualificationSnapshot(
        announcement_id=1,
        status=status,
        has_qualification=has_qualification,
        qualification_finished=qualification_finished,
        participants=participants or [],
    )


def test_decision_ranks_by_score_desc_and_registration_time():
    now = datetime.now(timezone.utc)
    snapshot = _snapshot(
        participants=[
            _participant(1, score=80, created_at=now + timedelta(seconds=2)),
            _participant(2, score=90, created_at=now + timedelta(seconds=3)),
            _participant(3, score=80, created_at=now + timedelta(seconds=1)),
            _participant(4, score=None, created_at=now),
        ]
    )

    decision = FinalizeAnnouncementQualificationDecisions().make(snapshot)

    assert decision.bracket_size == 4
    assert [
        (participant.participant_id, participant.qualification_rank)
        for participant in decision.participant_decisions
    ] == [(2, 1), (3, 2), (1, 3), (4, 4)]
    assert decision.participant_decisions[-1].is_qualified is False


def test_decision_rejects_non_live_status():
    snapshot = _snapshot(
        status=AnnouncementStatus.REGISTRATION_CLOSED,
        participants=[_participant(1, score=10), _participant(2, score=20)],
    )

    with pytest.raises(ValidationException, match="finalize_qualification"):
        FinalizeAnnouncementQualificationDecisions().make(snapshot)


def test_decision_rejects_too_few_participants():
    snapshot = _snapshot(participants=[_participant(1, score=10)])

    with pytest.raises(ValidationException, match="At least 2 participants"):
        FinalizeAnnouncementQualificationDecisions().make(snapshot)
