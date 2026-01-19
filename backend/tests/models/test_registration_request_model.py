from sqlalchemy import Enum as SAEnum, Text
from enums.registration_status import RegistrationStatus
from models.registration_request import RegistrationRequest


def test_registration_request_table_and_columns():
    assert RegistrationRequest.__tablename__ == "registration_requests"
    cols = RegistrationRequest.__table__.columns
    assert "announcement_id" in cols
    assert "user_id" in cols
    assert "status" in cols
    assert "cancellation_reason" in cols


def test_status_is_enum_of_registration_status():
    col = RegistrationRequest.__table__.c["status"]
    assert isinstance(col.type, SAEnum)
    assert getattr(col.type, "enum_class", None) is RegistrationStatus


def test_cancellation_reason_is_text_and_nullable():
    col = RegistrationRequest.__table__.c["cancellation_reason"]
    assert isinstance(col.type, Text)
    assert col.nullable is True


def test_registration_request_has_form_responses_relationship():
    assert hasattr(RegistrationRequest, "form_responses")
    rel = RegistrationRequest.form_responses
    assert rel.property.back_populates == "registration_request"
