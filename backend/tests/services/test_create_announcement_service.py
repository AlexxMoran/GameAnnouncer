import pytest
from datetime import datetime, timedelta, timezone
from services.create_announcement_service import CreateAnnouncementService
from schemas.announcement import AnnouncementCreate
from schemas.registration_form import RegistrationFormCreate, FormFieldCreate
from models.announcement import Announcement
from models.game import Game
from enums import AnnouncementStatus, FieldType
from sqlalchemy import select
from models.registration_form import RegistrationForm
from models.form_field import FormField


@pytest.mark.asyncio
async def test_create_announcement_without_form(db_session, create_user):
    """Test creating announcement without registration form."""
    user = await create_user(email="organizer@example.com")
    game = Game(name="Test Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    announcement_in = AnnouncementCreate(
        title="Test Tournament",
        content="Test content",
        game_id=game.id,
        registration_start_at=now + timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
    )

    service = CreateAnnouncementService(
        session=db_session, announcement_in=announcement_in, user=user
    )

    result = await service.call()

    assert isinstance(result, Announcement)
    assert result.title == "Test Tournament"
    assert result.organizer_id == user.id
    assert result.status == AnnouncementStatus.PRE_REGISTRATION
    assert result.registration_form is None


@pytest.mark.asyncio
async def test_create_announcement_with_registration_form(db_session, create_user):
    """Test creating announcement with custom registration form."""
    user = await create_user(email="organizer2@example.com")
    game = Game(name="Test Game 2", category="MOBA", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)

    form_fields = [
        FormFieldCreate(
            label="Discord Username",
            field_type=FieldType.TEXT,
            required=True,
            order=1,
        ),
        FormFieldCreate(
            label="Experience Level",
            field_type=FieldType.SELECT,
            required=True,
            options=["Beginner", "Intermediate", "Advanced"],
            order=2,
        ),
    ]

    registration_form = RegistrationFormCreate(fields=form_fields)

    announcement_in = AnnouncementCreate(
        title="Pro Tournament",
        content="For experienced players",
        game_id=game.id,
        registration_start_at=now + timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=20,
        registration_form=registration_form,
    )

    service = CreateAnnouncementService(
        session=db_session, announcement_in=announcement_in, user=user
    )

    result = await service.call()

    assert isinstance(result, Announcement)
    assert result.title == "Pro Tournament"
    assert result.organizer_id == user.id

    # Check registration form was created
    form_result = await db_session.execute(
        select(RegistrationForm).where(RegistrationForm.announcement_id == result.id)
    )
    form = form_result.scalar_one_or_none()
    assert form is not None

    # Check form fields were created
    fields_result = await db_session.execute(
        select(FormField).where(FormField.form_id == form.id).order_by(FormField.order)
    )
    fields = list(fields_result.scalars().all())
    assert len(fields) == 2
    assert fields[0].label == "Discord Username"
    assert fields[0].field_type == FieldType.TEXT
    assert fields[0].required is True
    assert fields[1].label == "Experience Level"
    assert fields[1].field_type == FieldType.SELECT
    assert fields[1].options == ["Beginner", "Intermediate", "Advanced"]


@pytest.mark.asyncio
async def test_create_announcement_status_pre_registration(db_session, create_user):
    """Test announcement status is PRE_REGISTRATION when registration hasn't started."""
    user = await create_user(email="organizer3@example.com")
    game = Game(name="Test Game 3", category="FPS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    announcement_in = AnnouncementCreate(
        title="Future Tournament",
        content="Coming soon",
        game_id=game.id,
        registration_start_at=now + timedelta(hours=1),  # starts in future
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
    )

    service = CreateAnnouncementService(
        session=db_session, announcement_in=announcement_in, user=user
    )

    result = await service.call()

    assert result.status == AnnouncementStatus.PRE_REGISTRATION


@pytest.mark.asyncio
async def test_create_announcement_status_registration_open(db_session, create_user):
    """Test announcement status is REGISTRATION_OPEN when registration has started."""
    user = await create_user(email="organizer4@example.com")
    game = Game(name="Test Game 4", category="RPG", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    announcement_in = AnnouncementCreate(
        title="Open Tournament",
        content="Registration open now",
        game_id=game.id,
        registration_start_at=now - timedelta(hours=1),  # already started
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
    )

    service = CreateAnnouncementService(
        session=db_session, announcement_in=announcement_in, user=user
    )

    result = await service.call()

    assert result.status == AnnouncementStatus.REGISTRATION_OPEN


@pytest.mark.asyncio
async def test_create_announcement_with_empty_form_fields(db_session, create_user):
    """Test creating announcement with registration form but no fields."""
    user = await create_user(email="organizer5@example.com")
    game = Game(name="Test Game 5", category="Strategy", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    registration_form = RegistrationFormCreate(fields=[])

    announcement_in = AnnouncementCreate(
        title="Simple Tournament",
        content="No custom fields",
        game_id=game.id,
        registration_start_at=now + timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
        registration_form=registration_form,
    )

    service = CreateAnnouncementService(
        session=db_session, announcement_in=announcement_in, user=user
    )

    result = await service.call()

    assert isinstance(result, Announcement)
    assert result.title == "Simple Tournament"

    # No form should be created if fields are empty
    form_result = await db_session.execute(
        select(RegistrationForm).where(RegistrationForm.announcement_id == result.id)
    )
    form = form_result.scalar_one_or_none()
    assert form is None
