from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import insert

from src.database.models import Room
from src.database.repositories.abc import BaseRepository


class RoomCreate(BaseModel):
    id: int
    room_number: str
    description: str


class RoomRepository(BaseRepository[Room]):
    async def insert_or_update(self, room: RoomCreate) -> Room:
        statement = (
            insert(Room)
            .values(**room.model_dump())
            .on_conflict_do_update(index_elements=[Room.id], set_=room.model_dump())
            .returning(Room)
        )
        result = await self._execute(statement, commit=True)
        return result.scalar_one()
