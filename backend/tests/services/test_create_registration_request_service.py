import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from services.create_registration_request_service import (
    CreateRegistrationRequestService,
)
from schemas.registration_request import RegistrationRequestCreate
from models.announcement import Announcement
from models.game import Game
from models.registration_request import RegistrationRequest
from models.registration_form import RegistrationForm
from exceptions import ValidationException
from enums import AnnouncementFormat, SeedMethod


@pytest.mark.asyncio
async def test_create_registration_request_success(db_session, create_user):
    """Test successful creation of registration request when registration is open."""
    user = await create_user(email="test@example.com")
    game = Game(name="Test Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Test Announcement",
        content="Test content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now - timedelta(hours=1),  # started 1 hour ago
        registration_end_at=now + timedelta(hours=1),  # ends in 1 hour
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    registration_request_in = RegistrationRequestCreate(announcement_id=announcement.id)

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=announcement,
        user=user,
        registration_request_in=registration_request_in,
    )

    result = await service.call()

    assert isinstance(result, RegistrationRequest)
    assert result.user_id == user.id
    assert result.announcement_id == announcement.id


@pytest.mark.asyncio
async def test_create_registration_request_before_start(db_session, create_user):
    """Test that registration fails when registration hasn't started yet."""
    user = await create_user(email="early@example.com")
    game = Game(name="Future Game", category="MOBA", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Future Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now + timedelta(hours=1),  # starts in 1 hour
        registration_end_at=now + timedelta(hours=2),
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    registration_request_in = RegistrationRequestCreate(announcement_id=announcement.id)

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=announcement,
        user=user,
        registration_request_in=registration_request_in,
    )

    with pytest.raises(ValidationException) as exc_info:
        await service.call()

    assert "Registration is currently closed" in str(exc_info.value)
    assert exc_info.value.status_code == 422


@pytest.mark.asyncio
async def test_create_registration_request_after_end(db_session, create_user):
    """Test that registration fails when registration has already ended."""
    user = await create_user(email="late@example.com")
    game = Game(name="Past Game", category="FPS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Past Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now - timedelta(hours=2),  # started 2 hours ago
        registration_end_at=now - timedelta(hours=1),  # ended 1 hour ago
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    registration_request_in = RegistrationRequestCreate(announcement_id=announcement.id)

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=announcement,
        user=user,
        registration_request_in=registration_request_in,
    )

    with pytest.raises(ValidationException) as exc_info:
        await service.call()

    assert "Registration is currently closed" in str(exc_info.value)
    assert exc_info.value.status_code == 422


@pytest.mark.asyncio
async def test_create_registration_request_at_exact_start(db_session, create_user):
    """Test registration at exact start time."""
    user = await create_user(email="exact@example.com")
    game = Game(name="Exact Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="Exact Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now,  # starts now
        registration_end_at=now + timedelta(hours=1),
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    registration_request_in = RegistrationRequestCreate(announcement_id=announcement.id)

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=announcement,
        user=user,
        registration_request_in=registration_request_in,
    )

    result = await service.call()

    assert result.user_id == user.id
    assert result.announcement_id == announcement.id


@pytest.mark.asyncio
async def test_create_registration_request_with_form_responses(db_session, create_user):
    """Test successful creation with form responses."""
    from models.form_field import FormField
    from schemas.form_field_response import FormFieldResponseCreate
    from enums import FormFieldType

    user = await create_user(email="form@example.com")
    game = Game(name="Form Game", category="RPG", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    announcement = Announcement(
        title="Form Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now - timedelta(hours=1),
        registration_end_at=now + timedelta(hours=1),
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.flush()

    registration_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(registration_form)
    await db_session.flush()

    field1 = FormField(
        form_id=registration_form.id,
        field_type=FormFieldType.TEXT,
        label="Car Name",
        required=True,
    )
    field2 = FormField(
        form_id=registration_form.id,
        field_type=FormFieldType.NUMBER,
        label="Games Won",
        required=False,
    )
    db_session.add_all([field1, field2])
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
    announcement = result.scalar_one()

    registration_request_in = RegistrationRequestCreate(
        announcement_id=announcement.id,
        form_responses=[
            FormFieldResponseCreate(form_field_id=field1.id, value="BMW M3"),
            FormFieldResponseCreate(form_field_id=field2.id, value="42"),
        ],
    )

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=announcement,
        user=user,
        registration_request_in=registration_request_in,
    )

    result = await service.call()

    assert result.user_id == user.id
    assert result.announcement_id == announcement.id
    assert len(result.form_responses) == 2
    assert result.form_responses[0].value == "BMW M3"
    assert result.form_responses[0].form_field.label == "Car Name"
    assert result.form_responses[1].value == "42"
    assert result.form_responses[1].form_field.label == "Games Won"


@pytest.mark.asyncio
async def test_create_registration_request_missing_required_fields(
    db_session, create_user
):
    """Test validation error when required fields are missing."""
    from models.form_field import FormField
    from schemas.form_field_response import FormFieldResponseCreate
    from enums import FormFieldType

    user = await create_user(email="missing@example.com")
    game = Game(name="Required Game", category="RPG", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    announcement = Announcement(
        title="Required Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now - timedelta(hours=1),
        registration_end_at=now + timedelta(hours=1),
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.flush()

    registration_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(registration_form)
    await db_session.flush()

    field1 = FormField(
        form_id=registration_form.id,
        field_type=FormFieldType.TEXT,
        label="Car Name",
        required=True,
    )
    field2 = FormField(
        form_id=registration_form.id,
        field_type=FormFieldType.TEXT,
        label="Driver Name",
        required=True,
    )
    db_session.add_all([field1, field2])
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
    announcement = result.scalar_one()

    registration_request_in = RegistrationRequestCreate(
        announcement_id=announcement.id,
        form_responses=[
            FormFieldResponseCreate(form_field_id=field1.id, value="BMW M3"),
        ],
    )

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=announcement,
        user=user,
        registration_request_in=registration_request_in,
    )

    with pytest.raises(ValidationException) as exc_info:
        await service.call()

    assert "Missing required fields" in str(exc_info.value)
    assert "Driver Name" in str(exc_info.value)
    assert exc_info.value.status_code == 422


@pytest.mark.asyncio
async def test_create_registration_request_invalid_field_ids(db_session, create_user):
    """Test validation error when form_field_ids don't belong to announcement's form."""
    from models.form_field import FormField
    from schemas.form_field_response import FormFieldResponseCreate
    from enums import FormFieldType

    user = await create_user(email="invalid@example.com")
    game = Game(name="Invalid Game", category="RPG", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    announcement = Announcement(
        title="Invalid Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now - timedelta(hours=1),
        registration_end_at=now + timedelta(hours=1),
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.flush()

    registration_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(registration_form)
    await db_session.flush()

    field1 = FormField(
        form_id=registration_form.id,
        field_type=FormFieldType.TEXT,
        label="Car Name",
        required=True,
    )
    db_session.add(field1)
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
    announcement = result.scalar_one()

    invalid_field_id = 99999

    registration_request_in = RegistrationRequestCreate(
        announcement_id=announcement.id,
        form_responses=[
            FormFieldResponseCreate(form_field_id=field1.id, value="BMW M3"),
            FormFieldResponseCreate(form_field_id=invalid_field_id, value="Invalid"),
        ],
    )

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=announcement,
        user=user,
        registration_request_in=registration_request_in,
    )

    with pytest.raises(ValidationException) as exc_info:
        await service.call()

    assert "Invalid form field IDs" in str(exc_info.value)
    assert str(invalid_field_id) in str(exc_info.value)
    assert exc_info.value.status_code == 422


@pytest.mark.asyncio
async def test_create_registration_request_responses_without_form(
    db_session, create_user
):
    """Test error when sending form_responses but announcement has no form."""
    from schemas.form_field_response import FormFieldResponseCreate

    user = await create_user(email="noform@example.com")
    game = Game(name="No Form Game", category="RPG", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now()
    announcement = Announcement(
        title="No Form Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now - timedelta(hours=1),
        registration_end_at=now + timedelta(hours=1),
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.commit()
    await db_session.refresh(announcement)

    registration_request_in = RegistrationRequestCreate(
        announcement_id=announcement.id,
        form_responses=[
            FormFieldResponseCreate(form_field_id=123, value="Should Fail"),
        ],
    )

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=announcement,
        user=user,
        registration_request_in=registration_request_in,
    )

    with pytest.raises(ValidationException) as exc_info:
        await service.call()

    assert "does not have a registration form" in str(exc_info.value)
    assert exc_info.value.status_code == 422


@pytest.mark.asyncio
async def test_create_registration_request_with_optional_fields_only(
    db_session, create_user
):
    """Test successful creation when all fields are optional and none filled."""
    from models.form_field import FormField
    from enums import FormFieldType

    user = await create_user(email="optional@example.com")
    game = Game(name="Optional Game", category="RPG", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    announcement = Announcement(
        title="Optional Announcement",
        content="Content",
        game_id=game.id,
        organizer_id=user.id,
        registration_start_at=now - timedelta(hours=1),
        registration_end_at=now + timedelta(hours=1),
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )
    db_session.add(announcement)
    await db_session.flush()

    registration_form = RegistrationForm(announcement_id=announcement.id)
    db_session.add(registration_form)
    await db_session.flush()

    field1 = FormField(
        form_id=registration_form.id,
        field_type=FormFieldType.TEXT,
        label="Optional Field",
        required=False,
    )
    db_session.add(field1)
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
    announcement = result.scalar_one()

    registration_request_in = RegistrationRequestCreate(
        announcement_id=announcement.id, form_responses=[]
    )

    service = CreateRegistrationRequestService(
        session=db_session,
        announcement=announcement,
        user=user,
        registration_request_in=registration_request_in,
    )

    result = await service.call()

    assert result.user_id == user.id
    assert result.announcement_id == announcement.id
    assert len(result.form_responses) == 0
