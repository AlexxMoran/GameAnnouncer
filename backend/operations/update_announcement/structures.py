from dataclasses import dataclass
from datetime import datetime
from typing import Any

from enums import AnnouncementStatus, SeedMethod
from modules.registration.form_schemas import RegistrationFormCreate


@dataclass(frozen=True)
class UpdateAnnouncementSnapshot:
    announcement_id: int
    status: AnnouncementStatus
    start_at: datetime
    registration_start_at: datetime
    registration_end_at: datetime
    has_qualification: bool
    announcement_data: dict[str, Any]
    registration_form: RegistrationFormCreate | None


@dataclass(frozen=True)
class UpdateAnnouncementDecision:
    announcement_id: int
    announcement_data: dict[str, Any]
    registration_form: RegistrationFormCreate | None
    status: AnnouncementStatus
    seed_method: SeedMethod
    reject_active_registration_requests: bool
    delete_participants: bool
