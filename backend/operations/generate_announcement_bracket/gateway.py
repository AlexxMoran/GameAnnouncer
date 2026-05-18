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

    async def load(
        self,
        contract: GenerateAnnouncementBracketContract,
    ) -> GenerateAnnouncementBracketSnapshot:
        announcement = await self._load_announcement(contract.announcement_id)

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
        announcement = await self._load_announcement(decision.announcement_id)
        announcement.bracket_size = decision.bracket_size

        participant_by_id = {
            participant.id: participant for participant in announcement.participants
        }
        eligible_participants = []
        for seed_decision in decision.participant_seeds:
            participant = participant_by_id.get(seed_decision.participant_id)
            if participant is None:
                raise ValidationException("Participant not found")
            participant.seed = seed_decision.seed
            eligible_participants.append(participant)

        match_repo = MatchRepository(self._session)
        builder = BracketMatchBuilder(
            announcement_id=decision.announcement_id,
            third_place_match=decision.third_place_match,
        )
        await builder.call(
            eligible_participants,
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
