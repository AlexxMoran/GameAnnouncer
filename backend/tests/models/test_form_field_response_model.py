from sqlalchemy import Text
from models.form_field_response import FormFieldResponse


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
