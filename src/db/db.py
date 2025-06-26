from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}


engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = sessionmaker(engine, class_=AsyncSession, autocommit=False, autoflush=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]: 
    """
    Dependency to get database session.

    Yields:
        AsyncSession: Database session for request lifecycle
    """
    async with async_session_maker() as session: 
        yield session 


AsyncSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


class Base(DeclarativeBase):
    pass
