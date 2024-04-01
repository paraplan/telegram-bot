from typing import Final
from uuid import UUID

from . import SingletonClient, get_parameters, read_query_file

INSERT: Final[str] = read_query_file("lesson/unconflict_insert.edgeql")
SELECT_BY_SCHEMA_ID: Final[str] = read_query_file("lesson/select_by_id.edgeql")
SELECT_BY_RELATIONS: Final[str] = read_query_file("lesson/select_by_relations.edgeql")


class LessonRepository:
    def __init__(self) -> None:
        self._client = SingletonClient.get_instance()

    async def get_by_id(self, id: UUID) -> list[object]:
        return await self._client.query(SELECT_BY_SCHEMA_ID, id=id)

    async def get_by_relations(self, cabinet_id: int, lecturer_id: int) -> list[object]:
        return await self._client.query(SELECT_BY_RELATIONS, **get_parameters(locals()))

    async def add(self, cabinet_id: int, lecturer_id: int) -> None:
        return await self._client.execute(INSERT, **get_parameters(locals()))

    async def add_or_select(self, cabinet_id: int, lecturer_id: int) -> list[object]:
        lessons = await self.get_by_relations(cabinet_id, lecturer_id)
        if lessons == []:
            await self.add(cabinet_id, lecturer_id)
            lessons = await self.get_by_relations(cabinet_id, lecturer_id)
        return lessons
