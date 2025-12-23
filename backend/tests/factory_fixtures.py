from pytest_factoryboy import register
import pytest_asyncio
import pytest
from tests.factories.user_factory import UserDictFactory
from models.user import User
from core.user_manager import UserManager
from schemas.user import UserCreate

register(UserDictFactory, "user")


@pytest_asyncio.fixture
async def create_user(db_session):
    """Async helper fixture that persists a user via the project's user manager.

    This constructs a `UserCreate` and calls the app's `UserManager` to
    persist the user into the provided `db_session`.
    """

    async def _create(**overrides):
        data = UserDictFactory(**overrides)
        user_create = UserCreate(**data)

        user_db = User.get_db(db_session)
        manager = UserManager(user_db)
        return await manager.create(user_create, safe=True, request=None)

    return _create


@pytest_asyncio.fixture
async def user(create_user):
    return await create_user()


@pytest.fixture
def user_factory():
    return UserDictFactory
