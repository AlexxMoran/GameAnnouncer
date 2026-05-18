from enums import AnnouncementStatus
from exceptions import ValidationException
from modules.announcements.utils.bracket import (
    compute_bracket_size,
    compute_bracket_slots,
)
from operations.generate_announcement_bracket.structures import (
    BracketParticipantSnapshot,
    GenerateAnnouncementBracketDecision,
    GenerateAnnouncementBracketSnapshot,
    ParticipantSeedDecision,
)


class GenerateAnnouncementBracketDecisions:
    """Business rules for generating an announcement bracket."""

    def make(
        self,
        snapshot: GenerateAnnouncementBracketSnapshot,
    ) -> GenerateAnnouncementBracketDecision:
        if snapshot.has_existing_matches:
            raise ValidationException("Bracket has already been generated")

        eligible = self._eligible_participants(snapshot)
        if len(eligible) < 2:
            raise ValidationException(
                "At least 2 eligible participants are required to generate a bracket"
            )

        bracket_size = self._resolve_bracket_size(snapshot, eligible)
        return GenerateAnnouncementBracketDecision(
            announcement_id=snapshot.announcement_id,
            participant_seeds=[
                ParticipantSeedDecision(participant_id=participant.id, seed=seed)
                for seed, participant in enumerate(eligible, start=1)
            ],
            bracket_size=bracket_size,
            seeding_slots=compute_bracket_slots(bracket_size),
            third_place_match=snapshot.third_place_match,
        )

    def _eligible_participants(
        self,
        snapshot: GenerateAnnouncementBracketSnapshot,
    ) -> list[BracketParticipantSnapshot]:
        if snapshot.has_qualification:
            self._validate_qualification_status(snapshot)
            return sorted(
                [p for p in snapshot.participants if p.is_qualified],
                key=lambda p: (
                    p.qualification_rank
                    if p.qualification_rank is not None
                    else float("inf")
                ),
            )

        self._validate_direct_status(snapshot)
        return sorted(
            snapshot.participants,
            key=lambda p: p.created_at,
        )

    def _resolve_bracket_size(
        self,
        snapshot: GenerateAnnouncementBracketSnapshot,
        eligible: list[BracketParticipantSnapshot],
    ) -> int:
        if snapshot.has_qualification:
            if snapshot.bracket_size is None:
                raise ValidationException("Bracket size is not set")
            if len(eligible) > snapshot.bracket_size:
                raise ValidationException(
                    f"Qualified participants ({len(eligible)}) exceed bracket size ({snapshot.bracket_size})"
                )
            return snapshot.bracket_size
        return compute_bracket_size(len(eligible))

    @staticmethod
    def _validate_qualification_status(
        snapshot: GenerateAnnouncementBracketSnapshot,
    ) -> None:
        if not snapshot.qualification_finished:
            raise ValidationException(
                "Qualification must be finalized before generating the bracket"
            )
        if snapshot.status != AnnouncementStatus.LIVE:
            raise ValidationException(
                f"'generate_bracket' is not allowed when status is '{snapshot.status}'"
            )

    @staticmethod
    def _validate_direct_status(snapshot: GenerateAnnouncementBracketSnapshot) -> None:
        if snapshot.status != AnnouncementStatus.REGISTRATION_CLOSED:
            raise ValidationException(
                f"'generate_bracket' is not allowed when status is '{snapshot.status}'"
            )
