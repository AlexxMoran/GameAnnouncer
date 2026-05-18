from datetime import datetime, timedelta, timezone

import pytest

from enums import AnnouncementStatus, SeedMethod
from exceptions import ValidationException
from operations.update_announcement.decisions import UpdateAnnouncementDecisions
from operations.update_announcement.structures import UpdateAnnouncementSnapshot


def _snapshot(**overrides) -> UpdateAnnouncementSnapshot:
    now = datetime.now(timezone.utc)
    data = {
        "announcement_id": 1,
        "status": AnnouncementStatus.REGISTRATION_OPEN,
        "start_at": now + timedelta(days=2),
        "registration_start_at": now - timedelta(hours=1),
        "registration_end_at": now + timedelta(days=1),
        "has_qualification": False,
        "announcement_data": {},
        "registration_form": None,
    }
    data.update(overrides)
    return UpdateAnnouncementSnapshot(**data)


def test_decision_sets_seed_method_and_open_status():
    decision = UpdateAnnouncementDecisions().make(
        _snapshot(announcement_data={"has_qualification": True})
    )

    assert decision.status == AnnouncementStatus.REGISTRATION_OPEN
    assert decision.seed_method == SeedMethod.QUALIFICATION_SCORE
    assert decision.reject_active_registration_requests is True
    assert decision.delete_participants is True


def test_decision_sets_closed_status_from_updated_dates():
    now = datetime.now(timezone.utc)
    decision = UpdateAnnouncementDecisions().make(
        _snapshot(
            announcement_data={
                "registration_start_at": now - timedelta(days=2),
                "registration_end_at": now - timedelta(days=1),
                "start_at": now + timedelta(days=1),
            }
        )
    )

    assert decision.status == AnnouncementStatus.REGISTRATION_CLOSED


def test_decision_rejects_live_announcement():
    with pytest.raises(ValidationException, match="before the tournament starts"):
        UpdateAnnouncementDecisions().make(_snapshot(status=AnnouncementStatus.LIVE))
