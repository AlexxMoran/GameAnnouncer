from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from core.db import db

SessionDep = Annotated[AsyncSession, Depends(db.session_getter)]
 