from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

engine = create_async_engine(
    "postgresql+asyncpg://cism:password@db:5432/cism", echo=True
)

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
