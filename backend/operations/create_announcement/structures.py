from dataclasses import dataclass
from typing import Any

from enums import AnnouncementStatus, SeedMethod
from modules.registration.form_schemas import RegistrationFormCreate


@dataclass(frozen=True)
class CreateAnnouncementSnapshot:
    announcement_data: dict[str, Any]
    registration_form: RegistrationFormCreate | None
    organizer_id: int


@dataclass(frozen=True)
class CreateAnnouncementDecision:
    announcement_data: dict[str, Any]
    registration_form: RegistrationFormCreate | None
    status: AnnouncementStatus
    seed_method: SeedMethod
    organizer_id: int
