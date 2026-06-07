from collections.abc import AsyncIterator

import pytest
from sqlalchemy import JSON, BigInteger, Integer, event
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.frameworks_and_drivers.repositories_implementations.aync_sqlalchemy.models import (
    Base,
)
from src.frameworks_and_drivers.repositories_implementations.aync_sqlalchemy.task import (
    TaskSqlAlchemyRepository,
)


@event.listens_for(Base.metadata, "before_create")
def _use_sqlite_compatible_types(target, connection, **_kwargs) -> None:
    if connection.dialect.name != "sqlite":
        return
    for table in target.tables.values():
        for column in table.columns:
            if isinstance(column.type, JSONB):
                column.type = JSON()
            if isinstance(column.type, BigInteger) and column.primary_key:
                column.type = Integer()


@pytest.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def task_repository(db_session: AsyncSession) -> TaskSqlAlchemyRepository:
    return TaskSqlAlchemyRepository(db_session)
