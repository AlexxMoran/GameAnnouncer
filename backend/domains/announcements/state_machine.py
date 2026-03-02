from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession
from transitions.core import MachineError
from transitions.extensions.asyncio import AsyncMachine

from domains.announcements.repository import AnnouncementRepository
from enums import AnnouncementStatus, AnnouncementTrigger
from exceptions import ValidationException

if TYPE_CHECKING:
    from domains.announcements.model import Announcement


class AnnouncementStateMachine:
    """
    State machine for the announcement lifecycle.

    Enforces valid status transitions only. Authorization is the caller's
    responsibility and must be performed before firing a trigger.

    Usage:
        sm = AnnouncementStateMachine(announcement, session)
        await sm.fire(AnnouncementTrigger.START_QUALIFICATION)
    """

    states = [s.value for s in AnnouncementStatus]

    transitions = [
        {
            "trigger": AnnouncementTrigger.START_QUALIFICATION.value,
            "source": AnnouncementStatus.REGISTRATION_CLOSED.value,
            "dest": AnnouncementStatus.LIVE.value,
        },
        {
            "trigger": AnnouncementTrigger.FINALIZE_QUALIFICATION.value,
            "source": AnnouncementStatus.LIVE.value,
            "dest": AnnouncementStatus.LIVE.value,
        },
        {
            "trigger": AnnouncementTrigger.GENERATE_BRACKET.value,
            "source": AnnouncementStatus.REGISTRATION_CLOSED.value,
            "dest": AnnouncementStatus.LIVE.value,
        },
        {
            "trigger": AnnouncementTrigger.GENERATE_BRACKET.value,
            "source": AnnouncementStatus.LIVE.value,
            "dest": AnnouncementStatus.LIVE.value,
        },
        {
            "trigger": AnnouncementTrigger.AUTO_FINISH.value,
            "source": AnnouncementStatus.LIVE.value,
            "dest": AnnouncementStatus.FINISHED.value,
        },
        {
            "trigger": AnnouncementTrigger.CANCEL.value,
            "source": [
                AnnouncementStatus.PRE_REGISTRATION.value,
                AnnouncementStatus.REGISTRATION_OPEN.value,
                AnnouncementStatus.REGISTRATION_CLOSED.value,
                AnnouncementStatus.LIVE.value,
            ],
            "dest": AnnouncementStatus.CANCELLED.value,
        },
    ]

    def __init__(self, announcement: Announcement, session: AsyncSession) -> None:
        self._ann = announcement
        self._session = session
        AsyncMachine(
            model=self,
            states=self.states,
            transitions=self.transitions,
            initial=announcement.status.value,
            auto_transitions=False,
            ignore_invalid_triggers=False,
        )

    async def fire(self, trigger: AnnouncementTrigger) -> Announcement:
        """
        Fire a lifecycle trigger and persist the new status.

        Raises:
            ValidationException: If the trigger is not valid from the current status.
        """
        try:
            await getattr(self, trigger.value)()
        except MachineError:
            raise ValidationException(
                f"'{trigger.value}' is not allowed when status is '{self._ann.status}'"
            )
        self._ann.status = AnnouncementStatus(self.state)
        return await AnnouncementRepository(self._session).save(self._ann)
