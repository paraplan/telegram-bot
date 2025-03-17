import datetime

from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload

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
    async def merge(self, lesson: LessonCreate) -> None:
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
            .options(selectinload(Lesson.subject), selectinload(Lesson.time_slot))
        )
        async with self.sessionmaker() as session:
            result = await session.execute(statement)
        return list(result.scalars().all())

    async def delete(self, lesson_id: int) -> None:
        delete_statement = delete(Lesson).where(Lesson.id == lesson_id)
        await self._execute(delete_statement, commit=True)
