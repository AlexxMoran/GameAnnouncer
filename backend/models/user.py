from models.base import Base
from typing import TYPE_CHECKING
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(20), nullable=True)
    last_name: Mapped[str] = mapped_column(String(20), nullable=True)
    nickname: Mapped[str] = mapped_column(String(20), nullable=True)

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
