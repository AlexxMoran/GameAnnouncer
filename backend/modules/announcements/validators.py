from datetime import datetime, timezone
from typing import Protocol

from core.utils import as_utc
from enums import AnnouncementStatus
from exceptions import ValidationException


class AnnouncementUpdateSubject(Protocol):
    status: AnnouncementStatus | str
    start_at: datetime
    registration_start_at: datetime
    registration_end_at: datetime


PRE_START_STATUSES = {
    AnnouncementStatus.PRE_REGISTRATION,
    AnnouncementStatus.REGISTRATION_OPEN,
    AnnouncementStatus.REGISTRATION_CLOSED,
}


class AnnouncementValidator:
    """Validates announcement data for create and update operations."""

    def validate_create(self, data: dict) -> None:
        """Validate dates for a new announcement."""
        self._validate_dates(
            registration_start_at=data["registration_start_at"],
            registration_end_at=data["registration_end_at"],
            start_at=data["start_at"],
        )

    def validate_update(
        self, announcement: AnnouncementUpdateSubject, data: dict
    ) -> None:
        """Validate that the announcement can be updated and the new dates are valid."""
        now = datetime.now(timezone.utc)
        status = AnnouncementStatus(announcement.status)

        if status not in PRE_START_STATUSES or as_utc(announcement.start_at) <= now:
            raise ValidationException(
                "Announcement can only be updated before the tournament starts"
            )

        self._validate_dates(
            registration_start_at=data.get(
                "registration_start_at", announcement.registration_start_at
            ),
            registration_end_at=data.get(
                "registration_end_at", announcement.registration_end_at
            ),
            start_at=data.get("start_at", announcement.start_at),
        )

    def _validate_dates(
        self,
        registration_start_at: datetime,
        registration_end_at: datetime,
        start_at: datetime,
    ) -> None:
        now = datetime.now(timezone.utc)

        if as_utc(registration_start_at) >= as_utc(registration_end_at):
            raise ValidationException(
                "registration_start_at must be before registration_end_at"
            )

        if as_utc(start_at) < as_utc(registration_end_at):
            raise ValidationException(
                "start_at must be after or equal to registration_end_at"
            )

        if as_utc(start_at) <= now:
            raise ValidationException("start_at must be in the future")
