import datetime

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.database.models import Lesson, Schedule
from src.database.repositories.abc import BaseRepository


class LessonCreate(BaseModel):
    schedule_id: int
    subject_id: int
    teacher_id: int | None = None
    room_id: int | None = None
    time_slot_id: int
    subgroup: int


class LessonRepository(BaseRepository[Lesson]):
    async def insert_or_update(self, lesson: LessonCreate) -> None:
        insert_statement = (
            insert(Lesson)
            .values(**lesson.model_dump())
            .on_conflict_do_update(
                index_elements=["schedule_id", "time_slot_id", "subgroup"],
                set_=lesson.model_dump(),
            )
        )
        await self._execute(insert_statement, commit=True)

    async def get(self, group_id: int, date: datetime.date) -> list[Lesson]:
        statement = (
            select(Lesson)
            .join(Schedule)
            .where(
                Schedule.group_id == group_id,
                Schedule.date == date,
            )
        )
        async with self.sessionmaker() as session:
            result = await session.execute(statement)
        return list(result.scalars().all())
