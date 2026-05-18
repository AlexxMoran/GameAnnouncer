from datetime import datetime, timezone

from core.utils import as_utc
from enums import AnnouncementStatus, SeedMethod
from modules.announcements.validators import AnnouncementValidator
from operations.create_announcement.structures import (
    CreateAnnouncementDecision,
    CreateAnnouncementSnapshot,
)


class CreateAnnouncementDecisions:
    """Business rules for creating an announcement."""

    def make(self, snapshot: CreateAnnouncementSnapshot) -> CreateAnnouncementDecision:
        AnnouncementValidator().validate_create(snapshot.announcement_data)

        has_qualification = snapshot.announcement_data["has_qualification"]
        registration_start_at = as_utc(
            snapshot.announcement_data["registration_start_at"]
        )

        return CreateAnnouncementDecision(
            announcement_data=snapshot.announcement_data,
            registration_form=snapshot.registration_form,
            status=(
                AnnouncementStatus.REGISTRATION_OPEN
                if registration_start_at <= datetime.now(timezone.utc)
                else AnnouncementStatus.PRE_REGISTRATION
            ),
            seed_method=(
                SeedMethod.QUALIFICATION_SCORE
                if has_qualification
                else SeedMethod.RANDOM
            ),
            organizer_id=snapshot.organizer_id,
        )
