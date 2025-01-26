import datetime

from pydantic import BaseModel
from sqlalchemy import insert, select

from src.database.models import Schedule
from src.database.repositories.abc import BaseRepository


class ScheduleCreate(BaseModel):
    group_id: int
    date: datetime.date


class ScheduleRepository(BaseRepository[Schedule]):
    async def insert_or_select(self, schedule: ScheduleCreate) -> Schedule:
        select_statement = select(Schedule).where(
            Schedule.date == schedule.date, Schedule.group_id == schedule.group_id
        )
        insert_statement = insert(Schedule).values(**schedule.model_dump())
        return await self._process_insert_or_select(select_statement, insert_statement)
