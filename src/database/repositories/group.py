import datetime

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload

from src.database.models import Group, Lesson, Room, Schedule, Subject, TimeSlot
from src.database.repositories.abc import BaseRepository


class GroupCreate(BaseModel):
    id: int
    name: str
    full_name: str
    course: int
    area_name: str


class GroupRepository(BaseRepository[Group]):
    async def insert_or_update(self, group: GroupCreate, join_students: bool = False) -> Group:
        """insert or update group by id"""
        statement = (
            insert(Group)
            .values(**group.model_dump())
            .on_conflict_do_update(index_elements=["id"], set_=group.model_dump())
            .returning(Group)
        )
        if join_students:
            statement = statement.options(selectinload(Group.users))
        result = await self._execute(statement, commit=True)
        return result.scalar_one()

    async def get_schedule(self, group_id: int, date: datetime.date) -> list[Lesson]:
        statement = (
            select(Lesson)
            .join(Schedule)
            .join(Subject)
            .join(TimeSlot)
            .join(Room, isouter=True)
            .where(
                Schedule.group_id == group_id,
                Schedule.date == date,
            )
            .options(
                selectinload(Lesson.time_slot),
                selectinload(Lesson.subject),
                selectinload(Lesson.room),
            )
            .order_by(TimeSlot.lesson_number)
        )
        async with self.sessionmaker() as session:
            result = await session.execute(statement)
            return list(result.scalars().all())

    async def get_all(self) -> list[Group]:
        statement = select(Group)
        async with self.sessionmaker() as session:
            result = await session.execute(statement)
            return list(result.scalars().all())

    async def get(self, id: int) -> Group:
        statement = select(Group).where(Group.id == id).options(selectinload(Group.users))
        async with self.sessionmaker() as session:
            result = await session.execute(statement)
            return result.scalar_one()
