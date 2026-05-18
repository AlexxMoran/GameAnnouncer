from datetime import datetime, timezone

from core.utils import as_utc
from enums import AnnouncementStatus, SeedMethod
from modules.announcements.validators import AnnouncementValidator
from operations.update_announcement.structures import (
    UpdateAnnouncementDecision,
    UpdateAnnouncementSnapshot,
)


class UpdateAnnouncementDecisions:
    """Business rules for updating an announcement before it starts."""

    def make(self, snapshot: UpdateAnnouncementSnapshot) -> UpdateAnnouncementDecision:
        AnnouncementValidator().validate_update(snapshot, snapshot.announcement_data)

        has_qualification = snapshot.announcement_data.get(
            "has_qualification",
            snapshot.has_qualification,
        )

        return UpdateAnnouncementDecision(
            announcement_id=snapshot.announcement_id,
            announcement_data=snapshot.announcement_data,
            registration_form=snapshot.registration_form,
            status=self._determine_status(snapshot),
            seed_method=(
                SeedMethod.QUALIFICATION_SCORE
                if has_qualification
                else SeedMethod.RANDOM
            ),
            reject_active_registration_requests=True,
            delete_participants=True,
        )

    @staticmethod
    def _determine_status(snapshot: UpdateAnnouncementSnapshot) -> AnnouncementStatus:
        now = datetime.now(timezone.utc)
        registration_start_at = as_utc(
            snapshot.announcement_data.get(
                "registration_start_at",
                snapshot.registration_start_at,
            )
        )
        registration_end_at = as_utc(
            snapshot.announcement_data.get(
                "registration_end_at",
                snapshot.registration_end_at,
            )
        )

        if registration_start_at > now:
            return AnnouncementStatus.PRE_REGISTRATION
        if registration_end_at > now:
            return AnnouncementStatus.REGISTRATION_OPEN
        return AnnouncementStatus.REGISTRATION_CLOSED
