from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import insert

from database.models import Subject
from database.repositories.abc import BaseRepository


class SubjectCreate(BaseModel):
    name: str


class SubjectRepository(BaseRepository[Subject]):
    async def insert_or_update(self, subject: SubjectCreate) -> Subject:
        statement = (
            insert(Subject)
            .values(**subject.model_dump())
            .on_conflict_do_update(index_elements=["name"], set_=subject.model_dump())
            .returning(Subject)
        )
        result = await self._execute(statement, commit=True)
        return result.scalar_one()
