from abc import ABC
from typing import Generic, TypeVar

from sqlalchemy import CursorResult, Insert, Select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.database.models import Base

T = TypeVar("T", bound=Base)


class ABCRepository(ABC, Generic[T]):
    sessionmaker: async_sessionmaker[AsyncSession]


class BaseRepository(ABCRepository[T], Generic[T]):
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self.sessionmaker = sessionmaker

    async def _execute(self, statement: Insert, commit: bool = False) -> CursorResult[T]:
        async with self.sessionmaker() as session:
            result = await session.execute(statement)
            if commit:
                await session.commit()
        return result

    async def _process_insert_or_select(
        self, select_statement: Select[tuple[T]], insert_statement: Insert
    ) -> T:
        async with self.sessionmaker() as session:
            result = await session.execute(select_statement)
            response = result.scalar_one_or_none()
            if response:
                return response
            await session.execute(insert_statement)
            await session.commit()
            result = await session.execute(select_statement)
            return result.scalar_one()
