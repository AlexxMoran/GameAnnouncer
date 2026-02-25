from sqlalchemy import Boolean, Enum as SAEnum, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from enums.registration_status import RegistrationStatus
from domains.registration.models import (
    RegistrationRequest,
    RegistrationForm,
    FormField,
    FormFieldResponse,
)


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


def test_registration_form_table_and_columns():
    assert RegistrationForm.__tablename__ == "registration_forms"
    cols = RegistrationForm.__table__.columns
    assert "announcement_id" in cols
    assert "id" in cols
    assert "created_at" in cols
    assert "updated_at" in cols


def test_announcement_id_is_unique():
    col = RegistrationForm.__table__.c["announcement_id"]
    assert col.unique is True
    assert col.nullable is False


def test_registration_form_has_announcement_relationship():
    assert hasattr(RegistrationForm, "announcement")
    rel = RegistrationForm.announcement
    assert rel.property.back_populates == "registration_form"
    assert rel.property.uselist is False


def test_registration_form_has_fields_relationship():
    assert hasattr(RegistrationForm, "fields")
    rel = RegistrationForm.fields
    assert rel.property.back_populates == "form"


def test_form_field_table_and_columns():
    assert FormField.__tablename__ == "form_fields"
    cols = FormField.__table__.columns
    assert "form_id" in cols
    assert "field_type" in cols
    assert "label" in cols
    assert "required" in cols
    assert "options" in cols


def test_field_type_is_enum():
    col = FormField.__table__.c["field_type"]
    assert isinstance(col.type, SAEnum)


def test_label_is_string_with_max_length():
    col = FormField.__table__.c["label"]
    assert isinstance(col.type, String)
    assert col.type.length == 200
    assert col.nullable is False


def test_required_is_boolean():
    col = FormField.__table__.c["required"]
    assert isinstance(col.type, Boolean)
    assert col.nullable is False


def test_options_is_jsonb_and_nullable():
    col = FormField.__table__.c["options"]
    assert isinstance(col.type, JSONB)
    assert col.nullable is True


def test_form_field_has_form_relationship():
    assert hasattr(FormField, "form")
    rel = FormField.form
    assert rel.property.back_populates == "fields"


def test_form_field_has_responses_relationship():
    assert hasattr(FormField, "responses")
    rel = FormField.responses
    assert rel.property.back_populates == "form_field"


def test_form_field_response_table_and_columns():
    assert FormFieldResponse.__tablename__ == "form_field_responses"
    cols = FormFieldResponse.__table__.columns
    assert "registration_request_id" in cols
    assert "form_field_id" in cols
    assert "value" in cols


def test_value_is_text():
    col = FormFieldResponse.__table__.c["value"]
    assert isinstance(col.type, Text)
    assert col.nullable is False


def test_form_field_response_has_unique_constraint():
    constraints = FormFieldResponse.__table__.constraints
    unique_constraints = [c for c in constraints if hasattr(c, "columns")]
    assert any(
        "registration_request_id" in [col.name for col in constraint.columns]
        and "form_field_id" in [col.name for col in constraint.columns]
        for constraint in unique_constraints
    )


def test_form_field_response_has_registration_request_relationship():
    assert hasattr(FormFieldResponse, "registration_request")
    rel = FormFieldResponse.registration_request
    assert rel.property.back_populates == "form_responses"


def test_form_field_response_has_form_field_relationship():
    assert hasattr(FormFieldResponse, "form_field")
    rel = FormFieldResponse.form_field
    assert rel.property.back_populates == "responses"
