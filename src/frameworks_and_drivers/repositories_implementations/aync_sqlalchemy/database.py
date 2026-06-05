from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.frameworks_and_drivers.repositories_implementations.aync_sqlalchemy.settings import (
    database_settings,
)

engine = create_async_engine(database_settings.url, echo=database_settings.echo)

async_database_session = sessionmaker(
    engine, autoflush=True, expire_on_commit=False, autobegin=True, class_=AsyncSession
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_database_session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        finally:
            await session.close()


get_db_async_context_manager = asynccontextmanager(get_async_db)
