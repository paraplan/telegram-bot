import datetime

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.database.models import TimeSlot
from src.database.repositories.abc import BaseRepository


class TimeSlotCreate(BaseModel):
    day_type_id: int
    start_time: datetime.time
    end_time: datetime.time
    lesson_number: int


class TimeSlotRepository(BaseRepository[TimeSlot]):
    async def insert_or_select(self, time_slot: TimeSlotCreate) -> TimeSlot:
        select_statement = select(TimeSlot).where(
            TimeSlot.day_type_id == time_slot.day_type_id,
            TimeSlot.start_time == time_slot.start_time,
            TimeSlot.end_time == time_slot.end_time,
            TimeSlot.lesson_number == time_slot.lesson_number,
        )
        insert_statement = insert(TimeSlot).values(**time_slot.model_dump())
        return await self._process_insert_or_select(select_statement, insert_statement)
