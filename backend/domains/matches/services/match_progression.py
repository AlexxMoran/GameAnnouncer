from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from core.permissions import authorize_action
from domains.announcements.model import Announcement
from domains.announcements.services.lifecycle import AnnouncementLifecycleService
from domains.matches.model import Match
from domains.matches.repository import MatchRepository
from domains.matches.schemas import MatchResultUpdate
from domains.participants.model import AnnouncementParticipant
from enums import MatchStatus
from exceptions import ValidationException


class MatchProgressionService:
    """
    Handles the result of a completed match.

    Responsibilities:
    - Validate the match can be completed
    - Set the winner and transition match to COMPLETED
    - Advance the winner into the next bracket match
    - Route the loser into the third-place match when applicable (semifinal)
    - Assign final placements for terminal matches (final and third-place)
    - Detect full tournament completion and trigger auto_finish
    """

    def __init__(
        self,
        match: Match,
        announcement: Announcement,
        result_in: MatchResultUpdate,
        session: AsyncSession,
        user,
    ) -> None:
        self._match = match
        self._announcement = announcement
        self._result_in = result_in
        self._session = session
        self._user = user
        self._repo = MatchRepository(session)

    async def call(self) -> Match:
        """Report a match result and progress the bracket."""
        authorize_action(self._user, self._announcement, "manage_lifecycle")

        self._validate()
        winner_id, loser_id = self._resolve_winner_and_loser_ids()

        self._match.winner_id = winner_id
        self._match.status = MatchStatus.COMPLETED
        self._match.completed_at = datetime.now(timezone.utc)

        next_match: Match | None = None
        if self._match.next_match_winner_id is not None:
            next_match = await self._repo.find_by_id(self._match.next_match_winner_id)
            if next_match is None:
                raise ValidationException("Next match not found")
            self._advance_to_next_match(next_match, winner_id)

        if next_match is not None and self._announcement.third_place_match:
            await self._maybe_fill_third_place(next_match, loser_id)

        await self._maybe_assign_placements(winner_id, loser_id)

        has_unfinished_matches = await self._repo.has_unfinished_non_bye_matches(
            self._announcement.id
        )
        if not has_unfinished_matches:
            await AnnouncementLifecycleService(
                self._announcement, self._session
            ).auto_finish()

        await self._session.flush()
        return self._match

    def _validate(self) -> None:
        """Validate preconditions before recording a result."""
        if self._match.status != MatchStatus.READY:
            raise ValidationException("Match is not ready")
        if self._match.is_bye:
            raise ValidationException("Cannot report result for a BYE match")

    def _resolve_winner_and_loser_ids(self) -> tuple[int, int]:
        """Resolve winner and loser IDs from the selected winner slot."""
        if self._result_in.winner == "participant1":
            winner_id = self._match.participant1_id
            loser_id = self._match.participant2_id
        else:
            winner_id = self._match.participant2_id
            loser_id = self._match.participant1_id

        if winner_id is None:
            raise ValidationException("Selected winner slot is empty")
        if loser_id is None:
            raise ValidationException("Match must have two participants")

        return winner_id, loser_id

    def _advance_to_next_match(self, next_match: Match, winner_id: int) -> None:
        """Place the winner into the correct slot of the next bracket match."""
        if self._match.match_number % 2 == 1:
            next_match.participant1_id = winner_id
        else:
            next_match.participant2_id = winner_id

        if (
            next_match.participant1_id is not None
            and next_match.participant2_id is not None
        ):
            next_match.status = MatchStatus.READY

    async def _maybe_fill_third_place(self, next_match: Match, loser_id: int) -> None:
        """
        Place the loser of a semifinal into the third-place match.

        A match is a semifinal when its next match is the final
        (i.e. next_match has no further next match).
        """
        if next_match.next_match_winner_id is not None:
            return

        third_place = await self._repo.find_third_place_match(self._announcement.id)
        if third_place is None:
            return

        if self._match.match_number % 2 == 1:
            third_place.participant1_id = loser_id
        else:
            third_place.participant2_id = loser_id

        if (
            third_place.participant1_id is not None
            and third_place.participant2_id is not None
        ):
            third_place.status = MatchStatus.READY

    async def _maybe_assign_placements(self, winner_id: int, loser_id: int) -> None:
        """Assign final placements when a terminal match (final or third-place) completes."""
        is_final = (
            self._match.next_match_winner_id is None and not self._match.is_third_place
        )

        if not is_final and not self._match.is_third_place:
            return

        winner_placement, loser_placement = (1, 2) if is_final else (3, 4)

        winner = await self._session.get(AnnouncementParticipant, winner_id)
        loser = await self._session.get(AnnouncementParticipant, loser_id)

        if winner is None or loser is None:
            raise ValidationException(
                "Participant record not found for placement assignment"
            )

        winner.placement = winner_placement
        loser.placement = loser_placement
