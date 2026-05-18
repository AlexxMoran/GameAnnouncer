from datetime import datetime, timedelta, timezone

import pytest

from enums import AnnouncementStatus, SeedMethod
from exceptions import ValidationException
from operations.create_announcement.decisions import CreateAnnouncementDecisions
from operations.create_announcement.structures import CreateAnnouncementSnapshot


def _snapshot(**overrides) -> CreateAnnouncementSnapshot:
    now = datetime.now(timezone.utc)
    data = {
        "title": "Tournament",
        "content": "Content",
        "game_id": 1,
        "registration_start_at": now + timedelta(hours=1),
        "registration_end_at": now + timedelta(days=1),
        "start_at": now + timedelta(days=2),
        "max_participants": 8,
        "format": "single_elimination",
        "has_qualification": False,
    }
    data.update(overrides)
    return CreateAnnouncementSnapshot(
        announcement_data=data,
        registration_form=None,
        organizer_id=1,
    )


def test_decision_sets_pre_registration_status_and_random_seed_method():
    decision = CreateAnnouncementDecisions().make(_snapshot())

    assert decision.status == AnnouncementStatus.PRE_REGISTRATION
    assert decision.seed_method == SeedMethod.RANDOM


def test_decision_sets_open_status_and_qualification_seed_method():
    now = datetime.now(timezone.utc)
    decision = CreateAnnouncementDecisions().make(
        _snapshot(
            registration_start_at=now - timedelta(hours=1),
            registration_end_at=now + timedelta(days=1),
            has_qualification=True,
        )
    )

    assert decision.status == AnnouncementStatus.REGISTRATION_OPEN
    assert decision.seed_method == SeedMethod.QUALIFICATION_SCORE


def test_decision_rejects_invalid_date_order():
    now = datetime.now(timezone.utc)
    snapshot = _snapshot(
        registration_start_at=now + timedelta(days=2),
        registration_end_at=now + timedelta(days=1),
    )

    with pytest.raises(ValidationException, match="registration_start_at"):
        CreateAnnouncementDecisions().make(snapshot)
