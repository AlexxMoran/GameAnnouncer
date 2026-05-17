import pytest
from datetime import datetime, timedelta
from sqlalchemy import select

from enums import AnnouncementFormat, FormFieldType, SeedMethod
from modules.announcements.model import Announcement
from modules.games.model import Game
from modules.registration.form_schemas import FormFieldCreate, RegistrationFormCreate
from modules.registration.models import FormField, RegistrationForm
from modules.registration.services.upsert_form import UpsertRegistrationFormService


def _make_announcement(game_id: int, organizer_id: int) -> Announcement:
    now = datetime.now()
    return Announcement(
        title="Test Tournament",
        content="Test content",
        game_id=game_id,
        organizer_id=organizer_id,
        registration_start_at=now + timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )


async def _create_announcement(db_session, create_user, email: str) -> Announcement:
    user = await create_user(email=email)
    game = Game(name=email, category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    announcement = _make_announcement(game.id, user.id)
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)
    return announcement


@pytest.mark.asyncio
async def test_create_new_registration_form(db_session, create_user):
    announcement = await _create_announcement(
        db_session, create_user, "organizer@example.com"
    )

    form_in = RegistrationFormCreate(
        fields=[
            FormFieldCreate(
                label="Discord Username",
                field_type=FormFieldType.TEXT,
                required=True,
            ),
            FormFieldCreate(
                label="Rank",
                field_type=FormFieldType.SELECT,
                required=False,
                options=["Bronze", "Silver", "Gold"],
            ),
        ]
    )
    result = await UpsertRegistrationFormService(
        session=db_session,
        announcement=announcement,
        registration_form_in=form_in,
    ).call()

    assert result.id is not None
    assert result.announcement_id == announcement.id
    assert announcement.registration_form is result
    assert len(result.fields) == 2
    assert result.fields[0].label == "Discord Username"
    assert result.fields[0].required is True
    assert result.fields[1].label == "Rank"
    assert result.fields[1].options == ["Bronze", "Silver", "Gold"]


@pytest.mark.asyncio
async def test_replace_existing_registration_form(db_session, create_user):
    announcement = await _create_announcement(
        db_session, create_user, "organizer2@example.com"
    )

    existing_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(existing_form)
    await db_session.flush()
    db_session.add(
        FormField(
            form_id=existing_form.id,
            label="Old Field",
            field_type=FormFieldType.TEXT,
            required=True,
        )
    )
    await db_session.commit()

    form_in = RegistrationFormCreate(
        fields=[
            FormFieldCreate(
                label="New Field",
                field_type=FormFieldType.TEXT,
                required=False,
            )
        ]
    )
    result = await UpsertRegistrationFormService(
        session=db_session,
        announcement=announcement,
        registration_form_in=form_in,
    ).call()

    forms_result = await db_session.execute(
        select(RegistrationForm).where(
            RegistrationForm.announcement_id == announcement.id
        )
    )
    forms = list(forms_result.scalars().all())
    assert len(forms) == 1
    assert forms[0].id == result.id
    assert len(result.fields) == 1
    assert result.fields[0].label == "New Field"

    fields_result = await db_session.execute(select(FormField))
    fields = list(fields_result.scalars().all())
    assert len(fields) == 1
    assert fields[0].label == "New Field"


@pytest.mark.asyncio
async def test_empty_fields_treated_as_no_form(db_session, create_user):
    announcement = await _create_announcement(
        db_session, create_user, "organizer3@example.com"
    )

    result = await UpsertRegistrationFormService(
        session=db_session,
        announcement=announcement,
        registration_form_in=RegistrationFormCreate(fields=[]),
    ).call()

    assert result is None
    assert announcement.registration_form is None


@pytest.mark.asyncio
async def test_delete_existing_registration_form(db_session, create_user):
    announcement = await _create_announcement(
        db_session, create_user, "organizer4@example.com"
    )

    existing_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(existing_form)
    await db_session.flush()
    db_session.add(
        FormField(
            form_id=existing_form.id,
            label="Old Field",
            field_type=FormFieldType.TEXT,
            required=True,
        )
    )
    await db_session.commit()

    result = await UpsertRegistrationFormService(
        session=db_session,
        announcement=announcement,
        registration_form_in=None,
    ).call()

    forms_result = await db_session.execute(
        select(RegistrationForm).where(
            RegistrationForm.announcement_id == announcement.id
        )
    )
    assert result is None
    assert forms_result.scalar_one_or_none() is None
    assert announcement.registration_form is None


@pytest.mark.asyncio
async def test_replace_with_empty_fields_removes_form(db_session, create_user):
    announcement = await _create_announcement(
        db_session, create_user, "organizer5@example.com"
    )

    existing_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(existing_form)
    await db_session.flush()
    db_session.add(
        FormField(
            form_id=existing_form.id,
            label="Old Field",
            field_type=FormFieldType.TEXT,
            required=True,
        )
    )
    await db_session.commit()

    result = await UpsertRegistrationFormService(
        session=db_session,
        announcement=announcement,
        registration_form_in=RegistrationFormCreate(fields=[]),
    ).call()

    forms_result = await db_session.execute(
        select(RegistrationForm).where(
            RegistrationForm.announcement_id == announcement.id
        )
    )
    fields_result = await db_session.execute(select(FormField))

    assert result is None
    assert forms_result.scalar_one_or_none() is None
    assert announcement.registration_form is None
    assert list(fields_result.scalars().all()) == []
