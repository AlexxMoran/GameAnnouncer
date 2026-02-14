from pytest_factoryboy import register
import pytest_asyncio
import pytest
from unittest.mock import patch, AsyncMock
from tests.factories import (
    UserDictFactory,
    AnnouncementDictFactory,
    RegistrationRequestDictFactory,
    GameDictFactory,
)
from models.user import User
from schemas.user import UserCreate
from pydantic import ValidationError

register(UserDictFactory, "user")
register(AnnouncementDictFactory, "announcement")
register(RegistrationRequestDictFactory, "registration_request")
register(GameDictFactory, "game")


@pytest_asyncio.fixture
async def create_user(db_session):
    """Async helper fixture that persists a user via the project's user manager.

    This constructs a `UserCreate` and calls the app's `UserManager` to
    persist the user into the provided `db_session`.
    """

    async def _create(**overrides):
        from core.user_manager import UserManager

        data = UserDictFactory(**overrides)

        try:
            user_create = UserCreate(**data)
        except ValidationError:
            email = data.get("email")
            if isinstance(email, str) and "@" in email:
                local, _ = email.split("@", 1)
                data["email"] = f"{local}@example.com"
                user_create = UserCreate(**data)
            else:
                raise

        user_db = User.get_db(db_session)
        manager = UserManager(user_db)

        with (
            patch("tasks.send_verification_email_task.kiq", new=AsyncMock()),
            patch("tasks.send_password_reset_email_task.kiq", new=AsyncMock()),
        ):
            created = await manager.create(user_create, safe=True, request=None)

        if overrides.get("is_verified"):
            created = await user_db.update(created, {"is_verified": True})

        return created

    return _create


@pytest_asyncio.fixture
async def user(create_user):
    return await create_user()


@pytest.fixture
def user_factory():
    return UserDictFactory


@pytest.fixture
def announcement_factory():
    return AnnouncementDictFactory


@pytest.fixture
def registration_request_factory():
    return RegistrationRequestDictFactory


@pytest.fixture
def game_factory():
    return GameDictFactory


@pytest_asyncio.fixture
async def create_announcement(db_session):
    """Async helper fixture that creates and persists an Announcement.

    Uses AnnouncementDictFactory for defaults, allowing field overrides.
    Similar to Rails FactoryBot pattern.
    """
    from models.announcement import Announcement
    from datetime import datetime

    async def _create(**overrides):
        factory_data = AnnouncementDictFactory.build()

        # Convert factory dict to model-compatible data
        data = {
            "title": factory_data["title"],
            "content": factory_data["content"],
            "game_id": factory_data["game_id"],
            "organizer_id": factory_data["organizer_id"],
            "registration_start_at": (
                datetime.fromisoformat(factory_data["registration_start_at"])
                if isinstance(factory_data["registration_start_at"], str)
                else factory_data["registration_start_at"]
            ),
            "registration_end_at": (
                datetime.fromisoformat(factory_data["registration_end_at"])
                if isinstance(factory_data["registration_end_at"], str)
                else factory_data["registration_end_at"]
            ),
            "start_at": (
                datetime.fromisoformat(factory_data["start_at"])
                if isinstance(factory_data["start_at"], str)
                else factory_data["start_at"]
            ),
            "max_participants": factory_data["max_participants"],
            "format": factory_data["format"],
            "has_qualification": factory_data["has_qualification"],
            "seed_method": factory_data["seed_method"],
            "bracket_size": factory_data["bracket_size"],
            "third_place_match": factory_data["third_place_match"],
            "qualification_finished": factory_data["qualification_finished"],
        }

        # Override with any provided values
        data.update(overrides)

        # Create and persist
        announcement = Announcement(**data)
        db_session.add(announcement)
        await db_session.commit()
        await db_session.refresh(announcement)

        return announcement

    return _create
