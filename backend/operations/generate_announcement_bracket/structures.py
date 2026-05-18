from dataclasses import dataclass
from datetime import datetime

from enums import AnnouncementStatus


@dataclass(frozen=True)
class BracketParticipantSnapshot:
    id: int
    created_at: datetime
    is_qualified: bool
    qualification_rank: int | None


@dataclass(frozen=True)
class GenerateAnnouncementBracketSnapshot:
    announcement_id: int
    status: AnnouncementStatus
    has_qualification: bool
    qualification_finished: bool
    bracket_size: int | None
    third_place_match: bool
    participants: list[BracketParticipantSnapshot]
    has_existing_matches: bool


@dataclass(frozen=True)
class ParticipantSeedDecision:
    participant_id: int
    seed: int


@dataclass(frozen=True)
class GenerateAnnouncementBracketDecision:
    announcement_id: int
    participant_seeds: list[ParticipantSeedDecision]
    bracket_size: int
    seeding_slots: list[int]
    third_place_match: bool
