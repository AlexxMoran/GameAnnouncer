from typing import Annotated
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from core.user_manager import UserManager
from core.db.container import create_db
from core.config import get_settings, Settings


async def _session_getter_dep():
    async for session in create_db().session_getter():
        yield session


SessionDep = Annotated[AsyncSession, Depends(_session_getter_dep)]


async def get_user_db(session: SessionDep):
    from models.user import User

    yield User.get_db(session=session)


UserDbDep = Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]


async def get_user_manager(user_db: UserDbDep):
    yield UserManager(user_db)


UserManagerDep = Annotated[UserManager, Depends(get_user_manager)]


def get_settings_dep():
    return get_settings()


SettingsDep = Annotated[Settings, Depends(get_settings_dep)]
