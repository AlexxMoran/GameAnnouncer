from enums import AnnouncementStatus
from exceptions import ValidationException
from modules.announcements.utils.bracket import compute_bracket_size
from operations.finalize_announcement_qualification.structures import (
    FinalizeAnnouncementQualificationDecision,
    FinalizeAnnouncementQualificationSnapshot,
    QualificationParticipantDecision,
    QualificationParticipantSnapshot,
)


class FinalizeAnnouncementQualificationDecisions:
    """Business rules for finalizing an announcement qualification stage."""

    def make(
        self,
        snapshot: FinalizeAnnouncementQualificationSnapshot,
    ) -> FinalizeAnnouncementQualificationDecision:
        self._validate(snapshot)

        bracket_size = compute_bracket_size(len(snapshot.participants))
        participant_decisions = [
            QualificationParticipantDecision(
                participant_id=participant.id,
                qualification_rank=rank,
                is_qualified=(
                    rank <= bracket_size and participant.qualification_score is not None
                ),
            )
            for rank, participant in enumerate(
                self._sorted_participants(snapshot.participants),
                start=1,
            )
        ]

        return FinalizeAnnouncementQualificationDecision(
            announcement_id=snapshot.announcement_id,
            bracket_size=bracket_size,
            participant_decisions=participant_decisions,
        )

    @staticmethod
    def _validate(snapshot: FinalizeAnnouncementQualificationSnapshot) -> None:
        if snapshot.status != AnnouncementStatus.LIVE:
            raise ValidationException(
                f"'finalize_qualification' is not allowed when status is '{snapshot.status}'"
            )

        if not snapshot.has_qualification:
            raise ValidationException(
                "This announcement does not have a qualification phase"
            )

        if snapshot.qualification_finished:
            raise ValidationException("Qualification has already been finalized")

        if len(snapshot.participants) < 2:
            raise ValidationException(
                "At least 2 participants are required to finalize qualification"
            )

    @staticmethod
    def _sorted_participants(
        participants: list[QualificationParticipantSnapshot],
    ) -> list[QualificationParticipantSnapshot]:
        return sorted(
            participants,
            key=lambda participant: (
                participant.qualification_score is None,
                -(participant.qualification_score or 0),
                participant.created_at,
            ),
        )
