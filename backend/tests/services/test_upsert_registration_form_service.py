import pytest
from datetime import datetime, timedelta
from services.upsert_registration_form_service import UpsertRegistrationFormService
from schemas.registration_form import RegistrationFormCreate, FormFieldCreate
from schemas.registration_request import RegistrationRequestCreate
from models.announcement import Announcement
from models.game import Game
from models.registration_form import RegistrationForm
from models.form_field import FormField
from models.registration_request import RegistrationRequest
from enums import FormFieldType, RegistrationStatus
from sqlalchemy import select
from api.v1.crud.registration_request import registration_request_crud


@pytest.mark.asyncio
async def test_create_new_registration_form(db_session, create_user):
    """Test creating a new registration form for announcement without existing form."""
    user = await create_user(email="organizer@example.com")
    game = Game(name="Test Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Test Tournament",
        content="Test content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now + timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    form_fields = [
        FormFieldCreate(
            label="Discord Username",
            key="discord_username",
            field_type=FormFieldType.TEXT,
            required=True,
            order=1,
        ),
    ]

    registration_form_in = RegistrationFormCreate(fields=form_fields)

    service = UpsertRegistrationFormService(
        session=db_session,
        announcement=announcement,
        registration_form_in=registration_form_in,
    )

    result = await service.call()

    assert isinstance(result, RegistrationForm)
    assert result.announcement_id == announcement.id

    # Check form fields were created
    fields_result = await db_session.execute(
        select(FormField).where(FormField.form_id == result.id)
    )
    fields = list(fields_result.scalars().all())
    assert len(fields) == 1
    assert fields[0].label == "Discord Username"


@pytest.mark.asyncio
async def test_update_existing_registration_form(db_session, create_user):
    """Test updating existing registration form replaces old form."""
    user = await create_user(email="organizer2@example.com")
    game = Game(name="Test Game 2", category="MOBA", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Test Tournament 2",
        content="Test content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now + timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    # Create initial form
    old_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(old_form)
    await db_session.flush()

    old_field = FormField(
        label="Old Field",
        key="old_field",
        field_type=FormFieldType.TEXT,
        required=False,
        form_id=old_form.id,
    )
    db_session.add(old_field)
    await db_session.commit()

    old_form_id = old_form.id

    await db_session.refresh(announcement)

    # Update with new form
    new_form_fields = [
        FormFieldCreate(
            label="New Field",
            key="new_field",
            field_type=FormFieldType.TEXT,
            required=True,
            order=1,
        ),
    ]

    registration_form_in = RegistrationFormCreate(fields=new_form_fields)

    service = UpsertRegistrationFormService(
        session=db_session,
        announcement=announcement,
        registration_form_in=registration_form_in,
    )

    result = await service.call()

    # Old form should be deleted
    old_form_result = await db_session.execute(
        select(RegistrationForm).where(RegistrationForm.id == old_form_id)
    )
    assert old_form_result.scalar_one_or_none() is None

    # New form should exist
    assert isinstance(result, RegistrationForm)
    assert result.id != old_form_id

    # Check new fields
    fields_result = await db_session.execute(
        select(FormField).where(FormField.form_id == result.id)
    )
    fields = list(fields_result.scalars().all())
    assert len(fields) == 1
    assert fields[0].label == "New Field"


@pytest.mark.asyncio
async def test_update_form_cancels_pending_requests(db_session, create_user):
    """Test that updating form cancels all pending registration requests."""
    organizer = await create_user(email="organizer3@example.com")
    participant = await create_user(email="participant@example.com")

    game = Game(name="Test Game 3", category="FPS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Test Tournament 3",
        content="Test content",
        game_id=game.id,
        organizer_id=organizer.id,
        registration_start_at=now - timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    # Create initial form
    old_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(old_form)
    await db_session.flush()

    old_field = FormField(
        label="Old Field",
        key="old_field",
        field_type=FormFieldType.TEXT,
        required=False,
        form_id=old_form.id,
    )
    db_session.add(old_field)
    await db_session.commit()

    # Create pending registration request
    rr_in = RegistrationRequestCreate(announcement_id=announcement.id)
    pending_request = await registration_request_crud.create(
        session=db_session, registration_request_in=rr_in, user=participant
    )

    assert pending_request.status == RegistrationStatus.PENDING

    await db_session.refresh(announcement)

    # Update form
    new_form_fields = [
        FormFieldCreate(
            label="Updated Field",
            key="updated_field",
            field_type=FormFieldType.TEXT,
            required=True,
            order=1,
        ),
    ]

    registration_form_in = RegistrationFormCreate(fields=new_form_fields)

    service = UpsertRegistrationFormService(
        session=db_session,
        announcement=announcement,
        registration_form_in=registration_form_in,
    )

    await service.call()

    # Check that pending request was cancelled
    await db_session.refresh(pending_request)
    assert pending_request.status == RegistrationStatus.CANCELLED
    assert pending_request.cancellation_reason is not None
    assert "Registration form has been updated" in pending_request.cancellation_reason


@pytest.mark.asyncio
async def test_update_form_cancels_approved_requests(db_session, create_user):
    """Test that updating form cancels approved registration requests."""
    organizer = await create_user(email="organizer4@example.com")
    participant = await create_user(email="participant2@example.com")

    game = Game(name="Test Game 4", category="Strategy", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Test Tournament 4",
        content="Test content",
        game_id=game.id,
        organizer_id=organizer.id,
        registration_start_at=now - timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    # Create initial form
    old_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(old_form)
    await db_session.commit()

    # Create approved registration request
    approved_request = RegistrationRequest(
        user_id=participant.id,
        announcement_id=announcement.id,
        status=RegistrationStatus.APPROVED,
    )
    db_session.add(approved_request)
    await db_session.commit()

    await db_session.refresh(announcement)

    # Update form
    new_form_fields = [
        FormFieldCreate(
            label="New Required Field",
            key="new_required_field",
            field_type=FormFieldType.TEXT,
            required=True,
            order=1,
        ),
    ]

    registration_form_in = RegistrationFormCreate(fields=new_form_fields)

    service = UpsertRegistrationFormService(
        session=db_session,
        announcement=announcement,
        registration_form_in=registration_form_in,
    )

    await service.call()

    # Check that approved request was cancelled
    await db_session.refresh(approved_request)
    assert approved_request.status == RegistrationStatus.CANCELLED
    assert approved_request.cancellation_reason is not None


@pytest.mark.asyncio
async def test_update_form_does_not_cancel_rejected_requests(db_session, create_user):
    """Test that updating form does not affect rejected requests."""
    organizer = await create_user(email="organizer5@example.com")
    participant = await create_user(email="participant3@example.com")

    game = Game(name="Test Game 5", category="RPG", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Test Tournament 5",
        content="Test content",
        game_id=game.id,
        organizer_id=organizer.id,
        registration_start_at=now - timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    # Create initial form
    old_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(old_form)
    await db_session.commit()

    # Create rejected registration request
    rejected_request = RegistrationRequest(
        user_id=participant.id,
        announcement_id=announcement.id,
        status=RegistrationStatus.REJECTED,
        cancellation_reason="Original rejection reason",
    )
    db_session.add(rejected_request)
    await db_session.commit()

    await db_session.refresh(announcement)

    # Update form
    new_form_fields = [
        FormFieldCreate(
            label="New Field",
            key="new_field",
            field_type=FormFieldType.TEXT,
            required=True,
            order=1,
        ),
    ]

    registration_form_in = RegistrationFormCreate(fields=new_form_fields)

    service = UpsertRegistrationFormService(
        session=db_session,
        announcement=announcement,
        registration_form_in=registration_form_in,
    )

    await service.call()

    # Check that rejected request remains unchanged
    await db_session.refresh(rejected_request)
    assert rejected_request.status == RegistrationStatus.REJECTED
    assert rejected_request.cancellation_reason == "Original rejection reason"


@pytest.mark.asyncio
async def test_create_form_with_multiple_fields(db_session, create_user):
    """Test creating form with multiple fields of different types."""
    user = await create_user(email="organizer6@example.com")
    game = Game(name="Test Game 6", category="Sports", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Test Tournament 6",
        content="Test content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now + timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    form_fields = [
        FormFieldCreate(
            label="Full Name",
            key="full_name",
            field_type=FormFieldType.TEXT,
            required=True,
            order=1,
        ),
        FormFieldCreate(
            label="Experience Level",
            key="experience_level",
            field_type=FormFieldType.SELECT,
            required=True,
            options={"choices": ["Beginner", "Intermediate", "Pro"]},
            order=2,
        ),
        FormFieldCreate(
            label="Comments",
            key="comments",
            field_type=FormFieldType.TEXTAREA,
            required=False,
            order=3,
        ),
    ]

    registration_form_in = RegistrationFormCreate(fields=form_fields)

    service = UpsertRegistrationFormService(
        session=db_session,
        announcement=announcement,
        registration_form_in=registration_form_in,
    )

    result = await service.call()

    # Check all fields were created correctly
    fields_result = await db_session.execute(
        select(FormField).where(FormField.form_id == result.id).order_by(FormField.id)
    )
    fields = list(fields_result.scalars().all())
    assert len(fields) == 3
    assert fields[0].label == "Full Name"
    assert fields[0].field_type == FormFieldType.TEXT
    assert fields[1].label == "Experience Level"
    assert fields[1].field_type == FormFieldType.SELECT
    assert fields[1].options == {"choices": ["Beginner", "Intermediate", "Pro"]}
    assert fields[2].label == "Comments"
    assert fields[2].field_type == FormFieldType.TEXTAREA
    assert fields[2].required is False
