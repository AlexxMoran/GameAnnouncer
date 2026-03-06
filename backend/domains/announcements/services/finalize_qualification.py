from sqlalchemy.ext.asyncio import AsyncSession

from core.permissions import authorize_action
from domains.announcements.model import Announcement
from domains.announcements.services.lifecycle import AnnouncementLifecycleService
from domains.announcements.utils.bracket import compute_bracket_size
from domains.participants.model import AnnouncementParticipant
from domains.users.model import User
from enums import AnnouncementStatus
from exceptions import ValidationException


class FinalizeQualificationService:
    """
    Finalizes the qualification phase for an announcement.

    Computes bracket size, assigns qualification ranks and qualified flags
    to all participants, then fires the lifecycle finalize_qualification trigger.

    Participants without a score are ranked last and are never marked as qualified,
    even if the computed bracket size would otherwise include their rank position.

    Usage:
        service = FinalizeQualificationService(announcement, session, user)
        announcement = await service.call()
        await session.commit()
    """

    def __init__(
        self, announcement: Announcement, session: AsyncSession, user: User
    ) -> None:
        self._announcement = announcement
        self._session = session
        self._user = user

    def _sorted_participants(self) -> list[AnnouncementParticipant]:
        """
        Sort participants by qualification score descending, then creation time ascending.

        Unscored participants (score is None) sort after all scored participants,
        ordered among themselves by registration time.
        """
        return sorted(
            self._announcement.participants,
            key=lambda p: (
                p.qualification_score is None,
                -(p.qualification_score or 0),
                p.created_at,
            ),
        )

    async def call(self) -> Announcement:
        """
        Rank participants, set qualified flags, compute bracket size, and finalize.

        Bracket size is computed from the total participant count. Only scored
        participants within the top bracket_size positions are marked as qualified.

        Raises:
            ValidationException: If the user is not authorized, the announcement is not
                                  in LIVE status, has_qualification is False, qualification
                                  is already finished, or there are no participants.
        """
        authorize_action(self._user, self._announcement, "manage_lifecycle")

        if self._announcement.status != AnnouncementStatus.LIVE:
            raise ValidationException(
                f"'finalize_qualification' is not allowed when status is '{self._announcement.status}'"
            )

        if not self._announcement.has_qualification:
            raise ValidationException(
                "This announcement does not have a qualification phase"
            )

        if self._announcement.qualification_finished:
            raise ValidationException("Qualification has already been finalized")

        participants = self._announcement.participants
        if len(participants) < 2:
            raise ValidationException(
                "At least 2 participants are required to finalize qualification"
            )

        sorted_participants = self._sorted_participants()
        bracket_size = compute_bracket_size(len(participants))

        for rank, participant in enumerate(sorted_participants, start=1):
            participant.qualification_rank = rank
            participant.is_qualified = (
                rank <= bracket_size and participant.qualification_score is not None
            )

        self._announcement.bracket_size = bracket_size
        self._announcement.qualification_finished = True

        await self._session.flush()

        lifecycle = AnnouncementLifecycleService(self._announcement, self._session)
        return await lifecycle.finalize_qualification()
