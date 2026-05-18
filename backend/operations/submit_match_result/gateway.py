from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from enums import MatchStatus
from exceptions import AppException, ValidationException
from modules.announcements.model import Announcement
from modules.announcements.services.lifecycle import AnnouncementLifecycleService
from modules.matches.model import Match
from modules.participants.model import AnnouncementParticipant
from operations.submit_match_result.contract import SubmitMatchResultContract
from operations.submit_match_result.structures import (
    MatchSnapshot,
    SubmitMatchResultDecision,
    SubmitMatchResultSnapshot,
)


class SubmitMatchResultGateway:
    """Translates between ORM state and match result operation data."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._match: Match | None = None
        self._announcement: Announcement | None = None

    async def load(
        self, contract: SubmitMatchResultContract
    ) -> SubmitMatchResultSnapshot:
        match = await self._load_match(contract.match_id)
        announcement = await self._load_announcement(match.announcement_id)
        self._match = match
        self._announcement = announcement
        next_match = (
            await self._load_match(match.next_match_winner_id)
            if match.next_match_winner_id is not None
            else None
        )
        third_place_match = (
            await self._load_third_place_match(announcement.id)
            if announcement.third_place_match
            else None
        )

        return SubmitMatchResultSnapshot(
            match=self._snapshot_match(match),
            announcement_id=announcement.id,
            third_place_match_enabled=announcement.third_place_match,
            selected_winner_slot=contract.winner,
            next_match=self._snapshot_match(next_match) if next_match else None,
            third_place_match=(
                self._snapshot_match(third_place_match) if third_place_match else None
            ),
            has_other_unfinished_non_bye_matches=await self._has_other_unfinished_non_bye_matches(
                announcement.id,
                match.id,
            ),
        )

    async def apply(self, decision: SubmitMatchResultDecision) -> Match:
        assert self._match is not None and self._announcement is not None, (
            "load() must be called before apply()"
        )
        match = self._match
        announcement = self._announcement

        match.winner_id = decision.winner_id
        match.status = MatchStatus.COMPLETED
        match.completed_at = datetime.now(timezone.utc)

        for assignment in decision.assignments:
            target_match = await self._load_match(assignment.match_id)
            if assignment.slot == "participant1":
                target_match.participant1_id = assignment.participant_id
            else:
                target_match.participant2_id = assignment.participant_id
            if assignment.mark_ready:
                target_match.status = MatchStatus.READY

        for placement in decision.placements:
            participant = await self._session.get(
                AnnouncementParticipant,
                placement.participant_id,
            )
            if participant is None:
                raise ValidationException(
                    "Participant record not found for placement assignment"
                )
            participant.placement = placement.placement

        if decision.auto_finish_announcement:
            await AnnouncementLifecycleService(
                announcement,
                self._session,
            ).auto_finish()

        await self._session.flush()
        return match

    @staticmethod
    def _snapshot_match(match: Match) -> MatchSnapshot:
        return MatchSnapshot(
            id=match.id,
            match_number=match.match_number,
            status=MatchStatus(match.status),
            participant1_id=match.participant1_id,
            participant2_id=match.participant2_id,
            next_match_winner_id=match.next_match_winner_id,
            is_bye=match.is_bye,
            is_third_place=match.is_third_place,
        )

    async def _load_match(self, match_id: int) -> Match:
        result = await self._session.execute(select(Match).where(Match.id == match_id))
        match = result.scalar_one_or_none()
        if match is None:
            raise AppException("Match not found", status_code=404)
        return match

    async def _load_announcement(self, announcement_id: int) -> Announcement:
        announcement = await self._session.get(Announcement, announcement_id)
        if announcement is None:
            raise AppException("Announcement not found", status_code=404)
        return announcement

    async def _load_third_place_match(self, announcement_id: int) -> Match | None:
        result = await self._session.execute(
            select(Match).where(
                Match.announcement_id == announcement_id,
                Match.is_third_place.is_(True),
            )
        )
        return result.scalar_one_or_none()

    async def _has_other_unfinished_non_bye_matches(
        self,
        announcement_id: int,
        current_match_id: int,
    ) -> bool:
        result = await self._session.execute(
            select(Match.id)
            .where(
                Match.announcement_id == announcement_id,
                Match.id != current_match_id,
                Match.is_bye.is_(False),
                Match.status != MatchStatus.COMPLETED,
            )
            .limit(1)
        )
        return result.scalar() is not None
