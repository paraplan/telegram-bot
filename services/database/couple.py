from datetime import datetime
from uuid import UUID

from database.queries.couple import insert

from . import BaseRepository, get_parameters


class CoupleRepository(BaseRepository):
    async def add(
        self,
        break_time: int,
        number: int,
        time_start: datetime,
        time_end: datetime,
        lesson_ids: list[UUID],
    ):
        return await insert(self._client, **get_parameters(locals()))
