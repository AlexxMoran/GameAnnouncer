import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from modules.announcements.model import Announcement
from modules.games.model import Game
from modules.registration.models import RegistrationRequest
from modules.users.model import User
from modules.registration.schemas import RegistrationRequestCreate
from modules.registration.repository import RegistrationRequestRepository
from operations.create_registration_request.contract import (
    CreateRegistrationRequestContract,
)
from operations.create_registration_request.scenario import (
    CreateRegistrationRequestScenario,
)
from exceptions import ValidationException
from enums import AnnouncementFormat, SeedMethod


async def _create_registration_request(db_session, user, registration_request_in):
    return await CreateRegistrationRequestScenario(db_session).run(
        CreateRegistrationRequestContract(
            registration_request_in=registration_request_in,
            user_id=user.id,
        )
    )


def _make_announcement(
    game_id: int, organizer_id: int, reg_open: bool = True
) -> Announcement:
    now = datetime.now(timezone.utc)
    reg_start = now - timedelta(hours=1) if reg_open else now + timedelta(hours=1)
    reg_end = reg_start + timedelta(hours=2)
    return Announcement(
        title="Test Announcement",
        content="Test content",
        game_id=game_id,
        organizer_id=organizer_id,
        registration_start_at=reg_start,
        registration_end_at=reg_end,
        start_at=now + timedelta(days=1),
        max_participants=10,
        format=AnnouncementFormat.SINGLE_ELIMINATION,
        has_qualification=False,
        seed_method=SeedMethod.RANDOM,
    )


@pytest.mark.asyncio
async def test_create_registration_request_success(db_session, create_user):
    """Successful creation when registration is open."""
    user = await create_user(email="test@example.com")
    game = Game(name="Test Game", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, reg_open=True)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    result = await _create_registration_request(
        db_session,
        user,
        RegistrationRequestCreate(announcement_id=ann.id),
    )

    assert isinstance(result, RegistrationRequest)
    assert result.user_id == user.id


@pytest.mark.asyncio
async def test_create_registration_request_closed_raises(db_session, create_user):
    """Registration raises ValidationException when closed."""
    user = await create_user(email="test2@example.com")
    game = Game(name="Test Game 2", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, reg_open=False)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    with pytest.raises(ValidationException) as exc_info:
        await _create_registration_request(
            db_session,
            user,
            RegistrationRequestCreate(announcement_id=ann.id),
        )

    assert "Registration is currently closed" in str(exc_info.value)


@pytest.mark.asyncio
async def test_create_registration_request_duplicate_raises(db_session, create_user):
    """Duplicate active request raises ValidationException."""
    user = await create_user(email="test3@example.com")
    game = Game(name="Test Game 3", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, reg_open=True)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    rr_in = RegistrationRequestCreate(announcement_id=ann.id)

    await _create_registration_request(db_session, user, rr_in)

    with pytest.raises(ValidationException) as exc_info:
        await _create_registration_request(db_session, user, rr_in)

    assert "already exists" in str(exc_info.value)


@pytest.mark.asyncio
async def test_create_registration_request_integrity_error_path_raises(
    engine, monkeypatch
):
    """DB-level duplicate insert is converted to ValidationException."""
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with session_factory() as session:
        user = User(
            email="integrity-path@example.com",
            hashed_password="hashed",
            is_active=True,
            is_superuser=False,
            is_verified=True,
        )
        game = Game(name="Test Game 4", category="RTS", description="Test")
        session.add_all([user, game])
        await session.commit()
        await session.refresh(user)
        await session.refresh(game)

        ann = _make_announcement(game.id, user.id, reg_open=True)
        session.add(ann)
        await session.commit()
        await session.refresh(ann)

        existing = RegistrationRequest(
            announcement_id=ann.id,
            user_id=user.id,
        )
        session.add(existing)
        await session.commit()

        async def no_existing_request(self, user_id, announcement_id):
            return None

        monkeypatch.setattr(
            RegistrationRequestRepository,
            "find_by_user_and_announcement",
            no_existing_request,
        )

        with pytest.raises(ValidationException) as exc_info:
            await _create_registration_request(
                session,
                user,
                RegistrationRequestCreate(announcement_id=ann.id),
            )

        assert "already exists" in str(exc_info.value)


@pytest.mark.asyncio
async def test_create_registration_request_non_duplicate_integrity_error_propagates(
    db_session, create_user, monkeypatch
):
    """Unexpected integrity failures should not be rewritten as duplicate-request errors."""
    user = await create_user(email="test5@example.com")
    game = Game(name="Test Game 5", category="RTS", description="Test")
    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    ann = _make_announcement(game.id, user.id, reg_open=True)
    db_session.add(ann)
    await db_session.commit()
    await db_session.refresh(ann)

    async def no_existing_request(self, user_id, announcement_id):
        return None

    monkeypatch.setattr(
        RegistrationRequestRepository,
        "find_by_user_and_announcement",
        no_existing_request,
    )

    async def raise_other_integrity_error():
        raise IntegrityError(
            "INSERT INTO registration_requests ...",
            {},
            Exception('duplicate key value violates unique constraint "other_index"'),
        )

    monkeypatch.setattr(db_session, "flush", raise_other_integrity_error)

    with pytest.raises(IntegrityError):
        await _create_registration_request(
            db_session,
            user,
            RegistrationRequestCreate(announcement_id=ann.id),
        )
