from sqlalchemy import Boolean, Enum as SAEnum, String
from sqlalchemy.dialects.postgresql import JSONB
from models.form_field import FormField


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
