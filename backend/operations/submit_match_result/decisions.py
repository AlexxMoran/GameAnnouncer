from exceptions import ValidationException
from enums import MatchStatus
from operations.submit_match_result.structures import (
    MatchSlotAssignmentDecision,
    MatchSnapshot,
    PlacementDecision,
    SubmitMatchResultDecision,
    SubmitMatchResultSnapshot,
)


class SubmitMatchResultDecisions:
    """Business rules for reporting a match result and progressing the bracket."""

    def make(self, snapshot: SubmitMatchResultSnapshot) -> SubmitMatchResultDecision:
        self._validate(snapshot.match)
        winner_id, loser_id = self._resolve_winner_and_loser_ids(snapshot)

        assignments = []
        if snapshot.next_match is not None:
            assignments.append(
                self._advance_to_next_match(
                    snapshot.match, snapshot.next_match, winner_id
                )
            )
            third_place_assignment = self._maybe_fill_third_place(
                snapshot,
                loser_id,
            )
            if third_place_assignment is not None:
                assignments.append(third_place_assignment)

        return SubmitMatchResultDecision(
            match_id=snapshot.match.id,
            winner_id=winner_id,
            assignments=assignments,
            placements=self._placement_decisions(snapshot.match, winner_id, loser_id),
            auto_finish_announcement=not snapshot.has_other_unfinished_non_bye_matches,
        )

    @staticmethod
    def _validate(match: MatchSnapshot) -> None:
        if match.status != MatchStatus.READY:
            raise ValidationException("Match is not ready")
        if match.is_bye:
            raise ValidationException("Cannot report result for a BYE match")

    @staticmethod
    def _resolve_winner_and_loser_ids(
        snapshot: SubmitMatchResultSnapshot,
    ) -> tuple[int, int]:
        if snapshot.selected_winner_slot == "participant1":
            winner_id = snapshot.match.participant1_id
            loser_id = snapshot.match.participant2_id
        else:
            winner_id = snapshot.match.participant2_id
            loser_id = snapshot.match.participant1_id

        if winner_id is None:
            raise ValidationException("Selected winner slot is empty")
        if loser_id is None:
            raise ValidationException("Match must have two participants")

        return winner_id, loser_id

    def _advance_to_next_match(
        self,
        match: MatchSnapshot,
        next_match: MatchSnapshot,
        winner_id: int,
    ) -> MatchSlotAssignmentDecision:
        slot = "participant1" if match.match_number % 2 == 1 else "participant2"
        return self._slot_assignment(next_match, slot, winner_id)

    def _maybe_fill_third_place(
        self,
        snapshot: SubmitMatchResultSnapshot,
        loser_id: int,
    ) -> MatchSlotAssignmentDecision | None:
        if not snapshot.third_place_match_enabled:
            return None
        if (
            snapshot.next_match is None
            or snapshot.next_match.next_match_winner_id is not None
        ):
            return None
        if snapshot.third_place_match is None:
            return None

        slot = (
            "participant1" if snapshot.match.match_number % 2 == 1 else "participant2"
        )
        return self._slot_assignment(snapshot.third_place_match, slot, loser_id)

    @staticmethod
    def _slot_assignment(
        target_match: MatchSnapshot,
        slot: str,
        participant_id: int,
    ) -> MatchSlotAssignmentDecision:
        participant1_id = (
            participant_id if slot == "participant1" else target_match.participant1_id
        )
        participant2_id = (
            participant_id if slot == "participant2" else target_match.participant2_id
        )
        return MatchSlotAssignmentDecision(
            match_id=target_match.id,
            slot=slot,
            participant_id=participant_id,
            mark_ready=participant1_id is not None and participant2_id is not None,
        )

    @staticmethod
    def _placement_decisions(
        match: MatchSnapshot,
        winner_id: int,
        loser_id: int,
    ) -> list[PlacementDecision]:
        is_final = match.next_match_winner_id is None and not match.is_third_place

        if not is_final and not match.is_third_place:
            return []

        winner_placement, loser_placement = (1, 2) if is_final else (3, 4)
        return [
            PlacementDecision(participant_id=winner_id, placement=winner_placement),
            PlacementDecision(participant_id=loser_id, placement=loser_placement),
        ]
