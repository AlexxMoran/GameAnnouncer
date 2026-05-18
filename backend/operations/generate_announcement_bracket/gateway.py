from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from enums import AnnouncementStatus
from exceptions import AppException, ValidationException
from modules.announcements.model import Announcement
from modules.announcements.services.lifecycle import AnnouncementLifecycleService
from modules.matches.repository import MatchRepository
from modules.matches.services.bracket_match_builder import BracketMatchBuilder
from operations.generate_announcement_bracket.contract import (
    GenerateAnnouncementBracketContract,
)
from operations.generate_announcement_bracket.structures import (
    BracketParticipantSnapshot,
    GenerateAnnouncementBracketDecision,
    GenerateAnnouncementBracketSnapshot,
)


class GenerateAnnouncementBracketGateway:
    """Translates between ORM state and bracket generation operation data."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._announcement: Announcement | None = None

    async def load(
        self,
        contract: GenerateAnnouncementBracketContract,
    ) -> GenerateAnnouncementBracketSnapshot:
        announcement = await self._load_announcement(contract.announcement_id)
        self._announcement = announcement

        match_repo = MatchRepository(self._session)
        has_existing_matches = await match_repo.exists_for_announcement(announcement.id)
        return GenerateAnnouncementBracketSnapshot(
            announcement_id=announcement.id,
            status=AnnouncementStatus(announcement.status),
            has_qualification=announcement.has_qualification,
            qualification_finished=announcement.qualification_finished,
            bracket_size=announcement.bracket_size,
            third_place_match=announcement.third_place_match,
            participants=[
                BracketParticipantSnapshot(
                    id=participant.id,
                    created_at=participant.created_at,
                    is_qualified=participant.is_qualified,
                    qualification_rank=participant.qualification_rank,
                )
                for participant in announcement.participants
            ],
            has_existing_matches=has_existing_matches,
        )

    async def apply(
        self,
        decision: GenerateAnnouncementBracketDecision,
    ) -> Announcement:
        """
        Apply the bracket decision: assign seeds, create matches, and advance the lifecycle.

        Match rows are flushed before the lifecycle transition so that the ORM assigns
        their IDs — the match builder needs those IDs to wire next_match_winner_id links.
        The lifecycle call must come after the flush for this reason.
        """
        assert self._announcement is not None, "load() must be called before apply()"
        announcement = self._announcement
        announcement.bracket_size = decision.bracket_size

        participant_by_id = {
            participant.id: participant for participant in announcement.participants
        }
        seeded_participants = []
        for seed_decision in decision.participant_seeds:
            participant = participant_by_id.get(seed_decision.participant_id)
            if participant is None:
                raise ValidationException("Participant not found")
            participant.seed = seed_decision.seed
            seeded_participants.append(participant)

        match_repo = MatchRepository(self._session)
        builder = BracketMatchBuilder(
            announcement_id=decision.announcement_id,
            third_place_match=decision.third_place_match,
        )
        await builder.call(
            seeded_participants,
            decision.bracket_size,
            decision.seeding_slots,
            match_repo,
        )
        await self._session.flush()

        lifecycle = AnnouncementLifecycleService(announcement, self._session)
        return await lifecycle.generate_bracket()

    async def _load_announcement(self, announcement_id: int) -> Announcement:
        result = await self._session.execute(
            select(Announcement)
            .options(selectinload(Announcement.participants))
            .where(Announcement.id == announcement_id)
        )
        announcement = result.scalar_one_or_none()
        if announcement is None:
            raise AppException("Announcement not found", status_code=404)
        return announcement
