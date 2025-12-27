from sqlalchemy import Enum as SAEnum
from enums.registration_status import RegistrationStatus
from models.registration_request import RegistrationRequest


def test_registration_request_table_and_columns():
    assert RegistrationRequest.__tablename__ == "registration_requests"
    cols = RegistrationRequest.__table__.columns
    assert "announcement_id" in cols
    assert "user_id" in cols
    assert "status" in cols


def test_status_is_enum_of_registration_status():
    col = RegistrationRequest.__table__.c["status"]
    assert isinstance(col.type, SAEnum)
    assert getattr(col.type, "enum_class", None) is RegistrationStatus
