import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy import select

from domains.announcements.model import Announcement
from domains.announcements.schemas import AnnouncementCreate
from domains.announcements.services.create import CreateAnnouncementService
from domains.registration.models import RegistrationForm, FormField
from domains.registration.schemas import RegistrationFormCreate, FormFieldCreate
from domains.games.model import Game
from enums import AnnouncementStatus, FormFieldType, AnnouncementFormat, SeedMethod


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
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
    )

    service = CreateAnnouncementService(
        session=db_session, announcement_in=announcement_in, user=user
    )
    result = await service.call()

    assert isinstance(result, Announcement)
    assert result.title == "Test Tournament"
    assert result.organizer_id == user.id
    assert result.status == AnnouncementStatus.PRE_REGISTRATION

    form_result = await db_session.execute(
        select(RegistrationForm).where(RegistrationForm.announcement_id == result.id)
    )
    assert form_result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_create_announcement_with_registration_form(db_session, create_user):
    """Test creating announcement with custom registration form."""
    user = await create_user(email="organizer2@example.com")
    game = Game(name="Test Game 2", category="MOBA", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    registration_form = RegistrationFormCreate(
        fields=[
            FormFieldCreate(
                label="Discord Username", field_type=FormFieldType.TEXT, required=True
            ),
            FormFieldCreate(
                label="Experience Level",
                field_type=FormFieldType.SELECT,
                required=True,
                options=["Beginner", "Intermediate", "Advanced"],
            ),
        ]
    )
    announcement_in = AnnouncementCreate(
        title="Pro Tournament",
        content="For experienced players",
        game_id=game.id,
        registration_start_at=now + timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=20,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        registration_form=registration_form,
        has_qualification=False,
    )

    service = CreateAnnouncementService(
        session=db_session, announcement_in=announcement_in, user=user
    )
    result = await service.call()

    assert result.title == "Pro Tournament"

    form_result = await db_session.execute(
        select(RegistrationForm).where(RegistrationForm.announcement_id == result.id)
    )
    form = form_result.scalar_one_or_none()
    assert form is not None

    fields_result = await db_session.execute(
        select(FormField).where(FormField.form_id == form.id).order_by(FormField.id)
    )
    fields = list(fields_result.scalars().all())
    assert len(fields) == 2
    assert fields[0].label == "Discord Username"
    assert fields[1].options == ["Beginner", "Intermediate", "Advanced"]


@pytest.mark.asyncio
async def test_create_announcement_status_pre_registration(db_session, create_user):
    """Status is PRE_REGISTRATION when registration hasn't started."""
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
        registration_start_at=now + timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
    )

    result = await CreateAnnouncementService(
        session=db_session, announcement_in=announcement_in, user=user
    ).call()

    assert result.status == AnnouncementStatus.PRE_REGISTRATION


@pytest.mark.asyncio
async def test_create_announcement_status_registration_open(db_session, create_user):
    """Status is REGISTRATION_OPEN when registration has started."""
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
        registration_start_at=now - timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
    )

    result = await CreateAnnouncementService(
        session=db_session, announcement_in=announcement_in, user=user
    ).call()

    assert result.status == AnnouncementStatus.REGISTRATION_OPEN


@pytest.mark.asyncio
async def test_create_announcement_seed_method_from_qualification(
    db_session, create_user
):
    """seed_method is derived from has_qualification flag."""
    user = await create_user(email="organizer7@example.com")
    game = Game(name="Test Game 7", category="MOBA", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    now = datetime.now(timezone.utc)
    announcement_in = AnnouncementCreate(
        title="Qualification Tournament",
        content="With qualification round",
        game_id=game.id,
        registration_start_at=now + timedelta(hours=1),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=2),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=True,
    )

    result = await CreateAnnouncementService(
        session=db_session, announcement_in=announcement_in, user=user
    ).call()

    assert result.has_qualification is True
    assert result.seed_method == SeedMethod.QUALIFICATION_SCORE
