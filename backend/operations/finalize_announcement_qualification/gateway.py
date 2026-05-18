from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from enums import AnnouncementStatus
from exceptions import AppException, ValidationException
from modules.announcements.model import Announcement
from modules.announcements.services.lifecycle import AnnouncementLifecycleService
from operations.finalize_announcement_qualification.contract import (
    FinalizeAnnouncementQualificationContract,
)
from operations.finalize_announcement_qualification.structures import (
    FinalizeAnnouncementQualificationDecision,
    FinalizeAnnouncementQualificationSnapshot,
    QualificationParticipantSnapshot,
)


class FinalizeAnnouncementQualificationGateway:
    """Translates between ORM state and qualification finalization data."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._announcement: Announcement | None = None

    async def load(
        self,
        contract: FinalizeAnnouncementQualificationContract,
    ) -> FinalizeAnnouncementQualificationSnapshot:
        announcement = await self._load_announcement(contract.announcement_id)
        self._announcement = announcement

        return FinalizeAnnouncementQualificationSnapshot(
            announcement_id=announcement.id,
            status=AnnouncementStatus(announcement.status),
            has_qualification=announcement.has_qualification,
            qualification_finished=announcement.qualification_finished,
            participants=[
                QualificationParticipantSnapshot(
                    id=participant.id,
                    created_at=participant.created_at,
                    qualification_score=participant.qualification_score,
                )
                for participant in announcement.participants
            ],
        )

    async def apply(
        self,
        decision: FinalizeAnnouncementQualificationDecision,
    ) -> Announcement:
        assert self._announcement is not None, "load() must be called before apply()"
        announcement = self._announcement
        participant_by_id = {
            participant.id: participant for participant in announcement.participants
        }

        for participant_decision in decision.participant_decisions:
            participant = participant_by_id.get(participant_decision.participant_id)
            if participant is None:
                raise ValidationException("Participant not found")
            participant.qualification_rank = participant_decision.qualification_rank
            participant.is_qualified = participant_decision.is_qualified

        announcement.bracket_size = decision.bracket_size
        announcement.qualification_finished = True

        await self._session.flush()

        lifecycle = AnnouncementLifecycleService(announcement, self._session)
        return await lifecycle.finalize_qualification()

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
