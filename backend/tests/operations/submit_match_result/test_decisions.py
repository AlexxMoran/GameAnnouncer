import pytest

from enums import MatchStatus
from exceptions import ValidationException
from operations.submit_match_result.decisions import SubmitMatchResultDecisions
from operations.submit_match_result.structures import (
    MatchSnapshot,
    SubmitMatchResultSnapshot,
)


def _match(
    match_id: int,
    *,
    match_number: int = 1,
    status: MatchStatus = MatchStatus.READY,
    participant1_id: int | None = 1,
    participant2_id: int | None = 2,
    next_match_winner_id: int | None = None,
    is_bye: bool = False,
    is_third_place: bool = False,
) -> MatchSnapshot:
    return MatchSnapshot(
        id=match_id,
        match_number=match_number,
        status=status,
        participant1_id=participant1_id,
        participant2_id=participant2_id,
        next_match_winner_id=next_match_winner_id,
        is_bye=is_bye,
        is_third_place=is_third_place,
    )


def _snapshot(
    *,
    match: MatchSnapshot | None = None,
    selected_winner_slot: str = "participant1",
    next_match: MatchSnapshot | None = None,
    third_place_match_enabled: bool = False,
    third_place_match: MatchSnapshot | None = None,
    has_other_unfinished_non_bye_matches: bool = True,
) -> SubmitMatchResultSnapshot:
    return SubmitMatchResultSnapshot(
        match=match or _match(1),
        announcement_id=1,
        third_place_match_enabled=third_place_match_enabled,
        selected_winner_slot=selected_winner_slot,
        next_match=next_match,
        third_place_match=third_place_match,
        has_other_unfinished_non_bye_matches=has_other_unfinished_non_bye_matches,
    )


def test_decision_advances_winner_to_next_match_and_marks_ready():
    snapshot = _snapshot(
        match=_match(1, match_number=2, next_match_winner_id=2),
        selected_winner_slot="participant2",
        next_match=_match(
            2, status=MatchStatus.PENDING, participant1_id=9, participant2_id=None
        ),
    )

    decision = SubmitMatchResultDecisions().make(snapshot)

    assert decision.winner_id == 2
    assert len(decision.assignments) == 1
    assert decision.assignments[0].match_id == 2
    assert decision.assignments[0].slot == "participant2"
    assert decision.assignments[0].participant_id == 2
    assert decision.assignments[0].mark_ready is True


def test_decision_routes_semifinal_loser_to_third_place_match():
    snapshot = _snapshot(
        match=_match(1, match_number=1, next_match_winner_id=2),
        next_match=_match(2, next_match_winner_id=None),
        third_place_match_enabled=True,
        third_place_match=_match(3, participant1_id=None, participant2_id=4),
    )

    decision = SubmitMatchResultDecisions().make(snapshot)

    third_place_assignment = decision.assignments[1]
    assert third_place_assignment.match_id == 3
    assert third_place_assignment.slot == "participant1"
    assert third_place_assignment.participant_id == 2
    assert third_place_assignment.mark_ready is True


def test_decision_assigns_final_placements_and_auto_finish():
    snapshot = _snapshot(has_other_unfinished_non_bye_matches=False)

    decision = SubmitMatchResultDecisions().make(snapshot)

    assert [(p.participant_id, p.placement) for p in decision.placements] == [
        (1, 1),
        (2, 2),
    ]
    assert decision.auto_finish_announcement is True


def test_decision_rejects_match_that_is_not_ready():
    snapshot = _snapshot(match=_match(1, status=MatchStatus.PENDING))

    with pytest.raises(ValidationException, match="not ready"):
        SubmitMatchResultDecisions().make(snapshot)
