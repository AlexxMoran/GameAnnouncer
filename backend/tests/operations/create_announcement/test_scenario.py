import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy import select

from modules.announcements.model import Announcement
from modules.announcements.schemas import AnnouncementCreate
from operations.create_announcement.contract import CreateAnnouncementContract
from operations.create_announcement.scenario import CreateAnnouncementScenario
from modules.registration.models import RegistrationForm, FormField
from modules.registration.form_schemas import RegistrationFormCreate, FormFieldCreate
from modules.games.model import Game
from enums import AnnouncementStatus, FormFieldType, AnnouncementFormat, SeedMethod


async def _create_announcement(db_session, announcement_in, user):
    return await CreateAnnouncementScenario(db_session).run(
        CreateAnnouncementContract(
            announcement_in=announcement_in,
            organizer_id=user.id,
        )
    )


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

    result = await _create_announcement(db_session, announcement_in, user)

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

    result = await _create_announcement(db_session, announcement_in, user)

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

    result = await _create_announcement(db_session, announcement_in, user)

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

    result = await _create_announcement(db_session, announcement_in, user)

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

    result = await _create_announcement(db_session, announcement_in, user)

    assert result.has_qualification is True
    assert result.seed_method == SeedMethod.QUALIFICATION_SCORE


@pytest.mark.asyncio
async def test_create_announcement_validates_date_order(db_session, create_user):
    """Validator rejects invalid date combinations on create."""
    user = await create_user(email="invalid-dates@example.com")
    game = Game(name="Test Game Val", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    from exceptions import ValidationException

    now = datetime.now(timezone.utc)
    announcement_in = AnnouncementCreate(
        title="Bad Dates",
        content="c",
        game_id=game.id,
        registration_start_at=now + timedelta(days=2),
        registration_end_at=now + timedelta(days=1),
        start_at=now + timedelta(days=3),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
    )

    with pytest.raises(
        ValidationException,
        match="registration_start_at must be before registration_end_at",
    ):
        await _create_announcement(db_session, announcement_in, user)
