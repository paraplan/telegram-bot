from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import insert

from src.database.models import DayType
from src.database.repositories.abc import BaseRepository


class DayTypeCreate(BaseModel):
    id: int
    name: str


class DayTypeRepository(BaseRepository[DayType]):
    async def insert(self, day_type: DayTypeCreate, ignore_conflict: bool = True) -> None:
        insert_statement = insert(DayType).values(**day_type.model_dump())
        if ignore_conflict:
            insert_statement = insert_statement.on_conflict_do_nothing()
        await self._execute(insert_statement, commit=True)
