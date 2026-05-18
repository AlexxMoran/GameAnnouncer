from dataclasses import dataclass
from datetime import datetime

from enums import AnnouncementStatus


@dataclass(frozen=True)
class QualificationParticipantSnapshot:
    id: int
    created_at: datetime
    qualification_score: int | None


@dataclass(frozen=True)
class FinalizeAnnouncementQualificationSnapshot:
    announcement_id: int
    status: AnnouncementStatus
    has_qualification: bool
    qualification_finished: bool
    participants: list[QualificationParticipantSnapshot]


@dataclass(frozen=True)
class QualificationParticipantDecision:
    participant_id: int
    qualification_rank: int
    is_qualified: bool


@dataclass(frozen=True)
class FinalizeAnnouncementQualificationDecision:
    announcement_id: int
    bracket_size: int
    participant_decisions: list[QualificationParticipantDecision]
