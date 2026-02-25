import pytest
from datetime import datetime, timedelta
from sqlalchemy import select

from domains.announcements.model import Announcement
from domains.games.model import Game
from domains.registration.models import RegistrationRequest, RegistrationForm, FormField
from domains.registration.schemas import (
    RegistrationFormCreate,
    FormFieldCreate,
)
from domains.registration.services.upsert_form import UpsertRegistrationFormService
from enums import FormFieldType, AnnouncementFormat, SeedMethod
from enums.registration_status import RegistrationStatus


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


@pytest.mark.asyncio
async def test_create_new_registration_form(db_session, create_user):
    """Creates a new form when none exists."""
    user = await create_user(email="organizer@example.com")
    game = Game(name="Test Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    form_in = RegistrationFormCreate(
        fields=[
            FormFieldCreate(
                label="Discord Username", field_type=FormFieldType.TEXT, required=True
            )
        ]
    )
    service = UpsertRegistrationFormService(
        session=db_session, announcement=ann, registration_form_in=form_in
    )
    result = await service.call()

    assert result.id is not None
    assert result.announcement_id == ann.id

    fields_result = await db_session.execute(
        select(FormField).where(FormField.form_id == result.id)
    )
    fields = list(fields_result.scalars().all())
    assert len(fields) == 1
    assert fields[0].label == "Discord Username"


@pytest.mark.asyncio
async def test_replace_existing_form_cancels_active_requests(db_session, create_user):
    """Replacing an existing form cancels all active registration requests."""
    organizer = await create_user(email="organizer2@example.com")
    applicant = await create_user(email="applicant@example.com")
    game = Game(name="Test Game 2", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, organizer.id)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    existing_form = RegistrationForm(announcement_id=ann.id)
    db_session.add(existing_form)
    await db_session.commit()

    rr = RegistrationRequest(
        announcement_id=ann.id,
        user_id=applicant.id,
        status=RegistrationStatus.PENDING,
    )
    db_session.add(rr)
    await db_session.commit()
    await db_session.refresh(rr)

    new_form_in = RegistrationFormCreate(
        fields=[
            FormFieldCreate(
                label="New Field", field_type=FormFieldType.TEXT, required=False
            )
        ]
    )
    service = UpsertRegistrationFormService(
        session=db_session, announcement=ann, registration_form_in=new_form_in
    )
    await service.call()

    await db_session.refresh(rr)
    assert rr.status == RegistrationStatus.CANCELLED
    assert rr.cancellation_reason is not None
