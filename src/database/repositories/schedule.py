import datetime

from pydantic import BaseModel
from sqlalchemy import insert, select

from src.database.models import Schedule
from src.database.repositories.abc import BaseRepository


class ScheduleCreate(BaseModel):
    group_id: int
    date: datetime.date


class ScheduleRepository(BaseRepository[Schedule]):
    async def create(self, schedule: ScheduleCreate) -> Schedule:
        insert_statement = insert(Schedule).values(**schedule.model_dump()).returning(Schedule)
        async with self.sessionmaker() as session:
            result = await session.execute(insert_statement)
            await session.commit()
            return result.scalar_one()

    async def select(self, schedule: ScheduleCreate) -> Schedule | None:
        select_statement = select(Schedule).where(
            Schedule.date == schedule.date, Schedule.group_id == schedule.group_id
        )
        async with self.sessionmaker() as session:
            result = await session.execute(select_statement)
        return result.scalar_one_or_none()
