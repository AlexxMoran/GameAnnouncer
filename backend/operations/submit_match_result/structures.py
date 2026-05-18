from dataclasses import dataclass
from typing import Literal

from enums import MatchStatus

MatchSlot = Literal["participant1", "participant2"]


@dataclass(frozen=True)
class MatchSnapshot:
    id: int
    match_number: int
    status: MatchStatus
    participant1_id: int | None
    participant2_id: int | None
    next_match_winner_id: int | None
    is_bye: bool
    is_third_place: bool


@dataclass(frozen=True)
class SubmitMatchResultSnapshot:
    match: MatchSnapshot
    announcement_id: int
    third_place_match_enabled: bool
    selected_winner_slot: MatchSlot
    next_match: MatchSnapshot | None
    third_place_match: MatchSnapshot | None
    has_other_unfinished_non_bye_matches: bool


@dataclass(frozen=True)
class MatchSlotAssignmentDecision:
    match_id: int
    slot: MatchSlot
    participant_id: int
    mark_ready: bool


@dataclass(frozen=True)
class PlacementDecision:
    participant_id: int
    placement: int


@dataclass(frozen=True)
class SubmitMatchResultDecision:
    match_id: int
    winner_id: int
    assignments: list[MatchSlotAssignmentDecision]
    placements: list[PlacementDecision]
    auto_finish_announcement: bool
