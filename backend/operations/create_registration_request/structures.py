from dataclasses import dataclass
from typing import Any

from modules.registration.form_schemas import FormFieldResponseCreate


@dataclass(frozen=True)
class RegistrationFormFieldSnapshot:
    id: int
    label: str
    required: bool


@dataclass(frozen=True)
class CreateRegistrationRequestSnapshot:
    announcement_id: int
    user_id: int
    request_data: dict[str, Any]
    form_responses: list[FormFieldResponseCreate]
    is_registration_open: bool
    has_existing_active_request: bool
    form_fields: list[RegistrationFormFieldSnapshot]


@dataclass(frozen=True)
class CreateRegistrationRequestDecision:
    request_data: dict[str, Any]
    user_id: int
    form_responses: list[FormFieldResponseCreate]
