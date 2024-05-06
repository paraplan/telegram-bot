from uuid import UUID

from database.queries.lesson import save_insert, select_by_id, select_by_relations

from . import BaseRepository, get_parameters


class LessonRepository(BaseRepository):
    async def get_by_id(self, id: UUID):
        return await select_by_id(self._client, **get_parameters(locals()))

    async def get_by_relations(self, cabinet_id: int, lecturer_id: int):
        return await select_by_relations(self._client, **get_parameters(locals()))

    async def add(self, cabinet_id: int, lecturer_id: int):
        return await save_insert(self._client, **get_parameters(locals()))

    async def add_or_select(self, cabinet_id: int, lecturer_id: int):
        lessons = await self.get_by_relations(cabinet_id, lecturer_id)
        if len(lessons) == 0:
            await self.add(cabinet_id, lecturer_id)
            lessons = await self.get_by_relations(cabinet_id, lecturer_id)
        return lessons
