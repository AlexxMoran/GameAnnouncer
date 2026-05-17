import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from enums import AnnouncementFormat, AnnouncementStatus, FormFieldType, SeedMethod
from enums.registration_status import RegistrationStatus
from exceptions import ValidationException
from modules.announcements.model import Announcement
from modules.announcements.schemas import AnnouncementUpdate
from modules.announcements.services.update import UpdateAnnouncementService
from modules.games.model import Game
from modules.participants.model import AnnouncementParticipant
from modules.participants.repository import ParticipantRepository
from modules.registration.form_schemas import FormFieldCreate, RegistrationFormCreate
from modules.registration.models import FormField, RegistrationForm, RegistrationRequest
from modules.registration.services.lifecycle import TOURNAMENT_UPDATED_REASON


async def _create_game(db_session) -> Game:
    game = Game(name="Update Service Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)
    return game


def _make_announcement(game_id: int, organizer_id: int) -> Announcement:
    now = datetime.now(timezone.utc)
    return Announcement(
        title="Original Tournament",
        content="Original content",
        game_id=game_id,
        organizer_id=organizer_id,
        status=AnnouncementStatus.REGISTRATION_OPEN,
        registration_start_at=now - timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=8,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )


@pytest.mark.asyncio
async def test_update_rejects_active_requests_and_replaces_form(
    db_session, create_user
):
    organizer = await create_user(email="update-organizer@example.com")
    pending_user = await create_user(email="pending-user@example.com")
    approved_user = await create_user(email="approved-user@example.com")
    game = await _create_game(db_session)

    announcement = _make_announcement(game.id, organizer.id)
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    existing_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(existing_form)
    await db_session.flush()
    db_session.add(
        FormField(
            form_id=existing_form.id,
            label="Old field",
            field_type=FormFieldType.TEXT,
            required=True,
        )
    )

    pending_request = RegistrationRequest(
        announcement_id=announcement.id,
        user_id=pending_user.id,
        status=RegistrationStatus.PENDING,
    )
    approved_request = RegistrationRequest(
        announcement_id=announcement.id,
        user_id=approved_user.id,
        status=RegistrationStatus.APPROVED,
    )
    participant = AnnouncementParticipant(
        announcement_id=announcement.id,
        user_id=approved_user.id,
        is_qualified=False,
    )
    db_session.add_all([pending_request, approved_request, participant])
    await db_session.commit()

    now = datetime.now(timezone.utc)
    update_in = AnnouncementUpdate(
        registration_start_at=now + timedelta(hours=2),
        registration_end_at=now + timedelta(days=2),
        start_at=now + timedelta(days=3),
        max_participants=16,
        registration_form=RegistrationFormCreate(
            fields=[
                FormFieldCreate(
                    label="New Discord",
                    field_type=FormFieldType.TEXT,
                    required=True,
                )
            ]
        ),
    )

    result = await UpdateAnnouncementService(
        session=db_session,
        announcement=announcement,
        announcement_in=update_in,
    ).call()

    await db_session.refresh(pending_request)
    await db_session.refresh(approved_request)

    assert result.max_participants == 16
    assert result.status == AnnouncementStatus.PRE_REGISTRATION
    assert pending_request.status == RegistrationStatus.REJECTED
    assert pending_request.cancellation_reason == TOURNAMENT_UPDATED_REASON
    assert approved_request.status == RegistrationStatus.REJECTED
    assert approved_request.cancellation_reason == TOURNAMENT_UPDATED_REASON

    participant_repo = ParticipantRepository(db_session)
    assert (
        await participant_repo.find_by_announcement_and_user(
            announcement.id, approved_user.id
        )
        is None
    )

    forms_result = await db_session.execute(
        select(RegistrationForm).where(
            RegistrationForm.announcement_id == announcement.id
        )
    )
    form = forms_result.scalar_one()
    fields_result = await db_session.execute(
        select(FormField).where(FormField.form_id == form.id)
    )
    fields = list(fields_result.scalars().all())
    assert len(fields) == 1
    assert fields[0].label == "New Discord"


@pytest.mark.asyncio
async def test_update_replaces_loaded_registration_form_fields(db_session, create_user):
    organizer = await create_user(email="loaded-form-organizer@example.com")
    game = await _create_game(db_session)

    announcement = _make_announcement(game.id, organizer.id)
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    existing_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(existing_form)
    await db_session.flush()
    db_session.add_all(
        [
            FormField(
                form_id=existing_form.id,
                label="Old Discord",
                field_type=FormFieldType.TEXT,
                required=True,
            ),
            FormField(
                form_id=existing_form.id,
                label="Old Rank",
                field_type=FormFieldType.TEXT,
                required=False,
            ),
        ]
    )
    await db_session.commit()

    loaded_result = await db_session.execute(
        select(Announcement)
        .options(
            selectinload(Announcement.registration_form).selectinload(
                RegistrationForm.fields
            )
        )
        .where(Announcement.id == announcement.id)
        .execution_options(populate_existing=True)
    )
    loaded_announcement = loaded_result.scalar_one()
    assert len(loaded_announcement.registration_form.fields) == 2

    await UpdateAnnouncementService(
        session=db_session,
        announcement=loaded_announcement,
        announcement_in=AnnouncementUpdate(
            registration_form=RegistrationFormCreate(
                fields=[
                    FormFieldCreate(
                        label="New Discord",
                        field_type=FormFieldType.TEXT,
                        required=True,
                    )
                ]
            )
        ),
    ).call()
    await db_session.commit()

    forms_result = await db_session.execute(
        select(RegistrationForm).where(
            RegistrationForm.announcement_id == announcement.id
        )
    )
    form = forms_result.scalar_one()
    fields_result = await db_session.execute(
        select(FormField).where(FormField.form_id == form.id)
    )
    fields = list(fields_result.scalars().all())
    assert len(fields) == 1
    assert fields[0].label == "New Discord"


@pytest.mark.asyncio
async def test_update_rejects_when_participant_limit_changes(db_session, create_user):
    organizer = await create_user(email="limit-organizer@example.com")
    applicant = await create_user(email="limit-applicant@example.com")
    game = await _create_game(db_session)

    announcement = _make_announcement(game.id, organizer.id)
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    request = RegistrationRequest(
        announcement_id=announcement.id,
        user_id=applicant.id,
        status=RegistrationStatus.PENDING,
    )
    db_session.add(request)
    await db_session.commit()

    await UpdateAnnouncementService(
        session=db_session,
        announcement=announcement,
        announcement_in=AnnouncementUpdate(max_participants=12),
    ).call()

    await db_session.refresh(request)
    assert request.status == RegistrationStatus.REJECTED
    assert request.cancellation_reason == TOURNAMENT_UPDATED_REASON


@pytest.mark.asyncio
async def test_update_changes_qualification_settings(db_session, create_user):
    organizer = await create_user(email="qualification-organizer@example.com")
    game = await _create_game(db_session)

    announcement = _make_announcement(game.id, organizer.id)
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    result = await UpdateAnnouncementService(
        session=db_session,
        announcement=announcement,
        announcement_in=AnnouncementUpdate(has_qualification=True),
    ).call()

    assert result.has_qualification is True
    assert result.seed_method == SeedMethod.QUALIFICATION_SCORE


@pytest.mark.asyncio
async def test_update_persists_frontend_payload_fields(db_session, create_user):
    organizer = await create_user(email="frontend-payload-organizer@example.com")
    game = await _create_game(db_session)

    announcement = _make_announcement(game.id, organizer.id)
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    now = datetime.now(timezone.utc)
    payload = {
        "content": "test for update",
        "has_qualification": True,
        "max_participants": 32,
        "registration_start_at": (now + timedelta(days=1)).isoformat(),
        "registration_end_at": (now + timedelta(days=2)).isoformat(),
        "start_at": (now + timedelta(days=2)).isoformat(),
        "title": "Tourik",
        "registration_form": {
            "fields": [
                {
                    "field_type": "text",
                    "label": "test",
                    "required": False,
                }
            ]
        },
    }

    await UpdateAnnouncementService(
        session=db_session,
        announcement=announcement,
        announcement_in=AnnouncementUpdate.model_validate(payload),
    ).call()
    await db_session.commit()

    result = await db_session.execute(
        select(Announcement)
        .options(
            selectinload(Announcement.registration_form).selectinload(
                RegistrationForm.fields
            )
        )
        .where(Announcement.id == announcement.id)
    )
    updated = result.scalar_one()

    assert updated.title == "Tourik"
    assert updated.content == "test for update"
    assert updated.has_qualification is True
    assert updated.seed_method == SeedMethod.QUALIFICATION_SCORE
    assert updated.max_participants == 32
    assert updated.registration_form is not None
    assert len(updated.registration_form.fields) == 1
    assert updated.registration_form.fields[0].field_type == FormFieldType.TEXT
    assert updated.registration_form.fields[0].label == "test"
    assert updated.registration_form.fields[0].required is False


@pytest.mark.asyncio
async def test_update_creates_registration_form_when_missing(db_session, create_user):
    organizer = await create_user(email="missing-form-organizer@example.com")
    game = await _create_game(db_session)

    announcement = _make_announcement(game.id, organizer.id)
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    await UpdateAnnouncementService(
        session=db_session,
        announcement=announcement,
        announcement_in=AnnouncementUpdate(
            registration_form=RegistrationFormCreate(
                fields=[
                    FormFieldCreate(
                        label="Nickname",
                        field_type=FormFieldType.TEXT,
                        required=True,
                    )
                ]
            )
        ),
    ).call()

    forms_result = await db_session.execute(
        select(RegistrationForm).where(
            RegistrationForm.announcement_id == announcement.id
        )
    )
    form = forms_result.scalar_one()
    fields_result = await db_session.execute(
        select(FormField).where(FormField.form_id == form.id)
    )
    fields = list(fields_result.scalars().all())
    assert len(fields) == 1
    assert fields[0].label == "Nickname"


@pytest.mark.asyncio
async def test_update_deletes_registration_form_when_null(db_session, create_user):
    organizer = await create_user(email="delete-form-organizer@example.com")
    game = await _create_game(db_session)

    announcement = _make_announcement(game.id, organizer.id)
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    existing_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(existing_form)
    await db_session.flush()
    db_session.add(
        FormField(
            form_id=existing_form.id,
            label="Old Nickname",
            field_type=FormFieldType.TEXT,
            required=True,
        )
    )
    await db_session.commit()

    await UpdateAnnouncementService(
        session=db_session,
        announcement=announcement,
        announcement_in=AnnouncementUpdate(registration_form=None),
    ).call()

    forms_result = await db_session.execute(
        select(RegistrationForm).where(
            RegistrationForm.announcement_id == announcement.id
        )
    )
    assert forms_result.scalar_one_or_none() is None
    assert announcement.registration_form is None


@pytest.mark.asyncio
async def test_update_replaces_registration_form_with_empty_fields(
    db_session, create_user
):
    organizer = await create_user(email="empty-form-organizer@example.com")
    applicant = await create_user(email="empty-form-applicant@example.com")
    game = await _create_game(db_session)

    announcement = _make_announcement(game.id, organizer.id)
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    existing_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(existing_form)
    await db_session.flush()
    db_session.add(
        FormField(
            form_id=existing_form.id,
            label="Old Nickname",
            field_type=FormFieldType.TEXT,
            required=True,
        )
    )
    request = RegistrationRequest(
        announcement_id=announcement.id,
        user_id=applicant.id,
        status=RegistrationStatus.PENDING,
    )
    db_session.add(request)
    await db_session.commit()

    await UpdateAnnouncementService(
        session=db_session,
        announcement=announcement,
        announcement_in=AnnouncementUpdate(
            registration_form=RegistrationFormCreate(fields=[])
        ),
    ).call()

    await db_session.refresh(request)
    assert request.status == RegistrationStatus.REJECTED

    forms_result = await db_session.execute(
        select(RegistrationForm).where(
            RegistrationForm.announcement_id == announcement.id
        )
    )
    assert forms_result.scalar_one_or_none() is None
    assert announcement.registration_form is None


@pytest.mark.asyncio
async def test_update_sets_registration_closed_status(db_session, create_user):
    organizer = await create_user(email="closed-status-organizer@example.com")
    game = await _create_game(db_session)

    announcement = _make_announcement(game.id, organizer.id)
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    now = datetime.now(timezone.utc)
    result = await UpdateAnnouncementService(
        session=db_session,
        announcement=announcement,
        announcement_in=AnnouncementUpdate(
            registration_start_at=now - timedelta(days=2),
            registration_end_at=now - timedelta(days=1),
            start_at=now + timedelta(days=1),
        ),
    ).call()

    assert result.status == AnnouncementStatus.REGISTRATION_CLOSED


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("update_in", "message"),
    [
        (
            AnnouncementUpdate(
                registration_start_at=datetime.now(timezone.utc) + timedelta(days=2),
                registration_end_at=datetime.now(timezone.utc) + timedelta(days=1),
            ),
            "registration_start_at must be before registration_end_at",
        ),
        (
            AnnouncementUpdate(
                registration_end_at=datetime.now(timezone.utc) + timedelta(days=3),
                start_at=datetime.now(timezone.utc) + timedelta(days=2),
            ),
            "start_at must be after or equal to registration_end_at",
        ),
        (
            AnnouncementUpdate(
                registration_start_at=datetime.now(timezone.utc) - timedelta(hours=3),
                registration_end_at=datetime.now(timezone.utc) - timedelta(hours=2),
                start_at=datetime.now(timezone.utc) - timedelta(hours=1),
            ),
            "start_at must be in the future",
        ),
    ],
)
async def test_update_validates_final_date_order(
    db_session, create_user, update_in, message
):
    organizer = await create_user(email=f"{message[:8]}@example.com")
    game = await _create_game(db_session)

    announcement = _make_announcement(game.id, organizer.id)
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    with pytest.raises(ValidationException) as exc_info:
        await UpdateAnnouncementService(
            session=db_session,
            announcement=announcement,
            announcement_in=update_in,
        ).call()

    assert message in str(exc_info.value)


@pytest.mark.asyncio
async def test_update_is_blocked_after_tournament_starts(db_session, create_user):
    organizer = await create_user(email="live-organizer@example.com")
    game = await _create_game(db_session)

    announcement = _make_announcement(game.id, organizer.id)
    announcement.status = AnnouncementStatus.LIVE
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    with pytest.raises(ValidationException) as exc_info:
        await UpdateAnnouncementService(
            session=db_session,
            announcement=announcement,
            announcement_in=AnnouncementUpdate(max_participants=12),
        ).call()

    assert "before the tournament starts" in str(exc_info.value)
