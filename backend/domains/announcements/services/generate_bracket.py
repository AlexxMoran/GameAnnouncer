from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from domains.announcements.model import Announcement
from domains.announcements.services.lifecycle import AnnouncementLifecycleService
from domains.announcements.utils.bracket import compute_bracket_size
from domains.matches.repository import MatchRepository
from domains.matches.services.bracket_match_builder import BracketMatchBuilder
from domains.participants.model import AnnouncementParticipant
from enums import AnnouncementStatus
from exceptions import ValidationException


class BracketStrategy(Protocol):
    """Interface for bracket generation strategies."""

    def validate(self) -> None: ...

    def get_eligible(self) -> list[AnnouncementParticipant]: ...

    def resolve_bracket_size(self, eligible: list[AnnouncementParticipant]) -> int: ...


class QualificationBracketStrategy:
    """
    Strategy for announcements with a qualification phase.

    Requires qualification to be finished and status LIVE.
    Eligible participants are those marked is_qualified, ordered by rank.
    Bracket size is taken from the announcement (already set during finalization).
    """

    def __init__(self, announcement: Announcement) -> None:
        self._announcement = announcement

    def validate(self) -> None:
        """
        Raises:
            ValidationException: If qualification is not finished or status is not LIVE.
        """
        if not self._announcement.qualification_finished:
            raise ValidationException(
                "Qualification must be finalized before generating the bracket"
            )
        if self._announcement.status != AnnouncementStatus.LIVE:
            raise ValidationException(
                f"'generate_bracket' is not allowed when status is '{self._announcement.status}'"
            )

    def get_eligible(self) -> list[AnnouncementParticipant]:
        """Return qualified participants sorted by qualification rank."""
        return sorted(
            [p for p in self._announcement.participants if p.is_qualified],
            key=lambda p: p.qualification_rank,
        )

    def resolve_bracket_size(self, eligible: list[AnnouncementParticipant]) -> int:
        """Return the bracket size already stored on the announcement."""
        return self._announcement.bracket_size


class DirectBracketStrategy:
    """
    Strategy for announcements without a qualification phase.

    Requires status REGISTRATION_CLOSED.
    All participants are eligible, ordered by registration time.
    Bracket size is computed from participant count and stored on the announcement.
    """

    def __init__(self, announcement: Announcement) -> None:
        self._announcement = announcement

    def validate(self) -> None:
        """
        Raises:
            ValidationException: If status is not REGISTRATION_CLOSED.
        """
        if self._announcement.status != AnnouncementStatus.REGISTRATION_CLOSED:
            raise ValidationException(
                f"'generate_bracket' is not allowed when status is '{self._announcement.status}'"
            )

    def get_eligible(self) -> list[AnnouncementParticipant]:
        """Return all participants sorted by registration time."""
        return sorted(
            self._announcement.participants,
            key=lambda p: p.created_at,
        )

    def resolve_bracket_size(self, eligible: list[AnnouncementParticipant]) -> int:
        """Compute bracket size from participant count and store it on the announcement."""
        bracket_size = compute_bracket_size(len(eligible))
        self._announcement.bracket_size = bracket_size
        return bracket_size


class GenerateBracketService:
    """
    Generates the single-elimination bracket for an announcement.

    Delegates mode-specific logic (validation, eligible participants, bracket size)
    to QualificationBracketStrategy or DirectBracketStrategy based on has_qualification.

    Creates Match records for all rounds, links them via next_match_winner_id,
    propagates BYE winners into round 2, and fires the generate_bracket lifecycle trigger.

    Usage:
        service = GenerateBracketService(announcement, session)
        announcement = await service.call()
        await session.commit()
    """

    def __init__(self, announcement: Announcement, session: AsyncSession) -> None:
        self._announcement = announcement
        self._session = session
        self._strategy: BracketStrategy = (
            QualificationBracketStrategy(announcement)
            if announcement.has_qualification
            else DirectBracketStrategy(announcement)
        )

    def _bracket_slots(self, size: int) -> list[int]:
        """
        Compute the standard single-elimination seeding order for a bracket of the given size.

        Returns a flat list of seeds where each consecutive pair of elements
        forms a first-round matchup. For example:
            size=2  → [1, 2]
            size=4  → [1, 4, 2, 3]
            size=8  → [1, 8, 4, 5, 2, 7, 3, 6]
        """
        if size == 2:
            return [1, 2]
        half = self._bracket_slots(size // 2)
        result = []
        for seed in half:
            result.append(seed)
            result.append(size + 1 - seed)
        return result

    def _assign_seeds(self, eligible: list[AnnouncementParticipant]) -> None:
        """Assign seeds 1..N to eligible participants in order."""
        for seed, participant in enumerate(eligible, start=1):
            participant.seed = seed

    async def call(self) -> Announcement:
        """
        Generate the bracket: assign seeds, build matches, link rounds, propagate BYEs.

        Raises:
            ValidationException: If preconditions fail or fewer than 2 eligible
                                  participants are found.
        """
        match_repo = MatchRepository(self._session)
        if await match_repo.exists_for_announcement(self._announcement.id):
            raise ValidationException("Bracket has already been generated")

        self._strategy.validate()

        eligible = self._strategy.get_eligible()
        if len(eligible) < 2:
            raise ValidationException(
                "At least 2 eligible participants are required to generate a bracket"
            )

        bracket_size = self._strategy.resolve_bracket_size(eligible)
        self._assign_seeds(eligible)
        seeding_slots = self._bracket_slots(bracket_size)

        builder = BracketMatchBuilder(
            announcement_id=self._announcement.id,
            third_place_match=self._announcement.third_place_match,
        )
        await builder.call(eligible, bracket_size, seeding_slots, match_repo)
        await self._session.flush()

        lifecycle = AnnouncementLifecycleService(self._announcement, self._session)
        return await lifecycle.generate_bracket()
