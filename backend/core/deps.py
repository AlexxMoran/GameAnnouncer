from typing import Annotated
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from schemas.filters.game_filter import GameFilter
from searches.game_search import GameSearch
from core.user_manager import UserManager
from core.db import db

SessionDep = Annotated[AsyncSession, Depends(db.session_getter)]


async def get_user_db(session: SessionDep):
    from models.user import User

    yield User.get_db(session=session)


UserDbDep = Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]


async def get_user_manager(user_db: UserDbDep):
    yield UserManager(user_db)


UserManagerDep = Annotated[UserManager, Depends(get_user_manager)]


async def get_game_search(session: SessionDep, filters: GameFilter = Depends()):
    return GameSearch(session=session, filters=filters)
