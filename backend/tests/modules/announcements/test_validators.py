import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

from enums import AnnouncementStatus
from exceptions import ValidationException
from modules.announcements.validators import AnnouncementValidator


def _future_dates(
    reg_start_delta=timedelta(hours=1),
    reg_end_delta=timedelta(days=1),
    start_delta=timedelta(days=2),
):
    now = datetime.now(timezone.utc)
    return {
        "registration_start_at": now + reg_start_delta,
        "registration_end_at": now + reg_end_delta,
        "start_at": now + start_delta,
    }


def _mock_announcement(
    status=AnnouncementStatus.REGISTRATION_OPEN,
    start_at_delta=timedelta(days=2),
    reg_start_delta=timedelta(hours=-1),
    reg_end_delta=timedelta(days=1),
):
    now = datetime.now(timezone.utc)
    ann = MagicMock()
    ann.status = status
    ann.start_at = now + start_at_delta
    ann.registration_start_at = now + reg_start_delta
    ann.registration_end_at = now + reg_end_delta
    return ann


class TestValidateCreate:
    def test_valid_dates_pass(self):
        AnnouncementValidator().validate_create(_future_dates())

    def test_reg_start_equal_to_reg_end_raises(self):
        now = datetime.now(timezone.utc)
        data = {
            "registration_start_at": now + timedelta(days=1),
            "registration_end_at": now + timedelta(days=1),
            "start_at": now + timedelta(days=2),
        }
        with pytest.raises(
            ValidationException,
            match="registration_start_at must be before registration_end_at",
        ):
            AnnouncementValidator().validate_create(data)

    def test_reg_start_after_reg_end_raises(self):
        now = datetime.now(timezone.utc)
        data = {
            "registration_start_at": now + timedelta(days=2),
            "registration_end_at": now + timedelta(days=1),
            "start_at": now + timedelta(days=3),
        }
        with pytest.raises(
            ValidationException,
            match="registration_start_at must be before registration_end_at",
        ):
            AnnouncementValidator().validate_create(data)

    def test_start_before_reg_end_raises(self):
        now = datetime.now(timezone.utc)
        data = {
            "registration_start_at": now + timedelta(hours=1),
            "registration_end_at": now + timedelta(days=2),
            "start_at": now + timedelta(days=1),
        }
        with pytest.raises(
            ValidationException,
            match="start_at must be after or equal to registration_end_at",
        ):
            AnnouncementValidator().validate_create(data)

    def test_start_in_past_raises(self):
        now = datetime.now(timezone.utc)
        data = {
            "registration_start_at": now - timedelta(days=3),
            "registration_end_at": now - timedelta(days=2),
            "start_at": now - timedelta(days=1),
        }
        with pytest.raises(ValidationException, match="start_at must be in the future"):
            AnnouncementValidator().validate_create(data)

    def test_start_equal_to_reg_end_is_valid(self):
        now = datetime.now(timezone.utc)
        data = {
            "registration_start_at": now + timedelta(hours=1),
            "registration_end_at": now + timedelta(days=1),
            "start_at": now + timedelta(days=1),
        }
        AnnouncementValidator().validate_create(data)


class TestValidateUpdate:
    def test_valid_update_passes(self):
        ann = _mock_announcement()
        AnnouncementValidator().validate_update(ann, _future_dates())

    def test_live_status_raises(self):
        ann = _mock_announcement(status=AnnouncementStatus.LIVE)
        with pytest.raises(ValidationException, match="before the tournament starts"):
            AnnouncementValidator().validate_update(ann, _future_dates())

    def test_finished_status_raises(self):
        ann = _mock_announcement(status=AnnouncementStatus.FINISHED)
        with pytest.raises(ValidationException, match="before the tournament starts"):
            AnnouncementValidator().validate_update(ann, _future_dates())

    def test_start_already_passed_raises(self):
        ann = _mock_announcement(
            status=AnnouncementStatus.PRE_REGISTRATION,
            start_at_delta=timedelta(hours=-1),
        )
        with pytest.raises(ValidationException, match="before the tournament starts"):
            AnnouncementValidator().validate_update(ann, {})

    def test_fallback_to_existing_dates_when_data_empty(self):
        ann = _mock_announcement()
        AnnouncementValidator().validate_update(ann, {})

    def test_partial_update_merges_with_existing_dates(self):
        ann = _mock_announcement()
        now = datetime.now(timezone.utc)
        AnnouncementValidator().validate_update(
            ann, {"start_at": now + timedelta(days=3)}
        )

    def test_invalid_dates_in_update_raises(self):
        ann = _mock_announcement()
        now = datetime.now(timezone.utc)
        data = {
            "registration_start_at": now + timedelta(days=2),
            "registration_end_at": now + timedelta(days=1),
        }
        with pytest.raises(
            ValidationException,
            match="registration_start_at must be before registration_end_at",
        ):
            AnnouncementValidator().validate_update(ann, data)
