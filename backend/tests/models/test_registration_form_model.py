from models.registration_form import RegistrationForm


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
