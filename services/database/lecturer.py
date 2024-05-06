from database.queries.lecturer import save_insert, select_by_schema_id

from . import BaseRepository, get_parameters


class LecturerRepository(BaseRepository):
    async def get_by_id(self, schema_id: int):
        return await select_by_schema_id(self._client, **get_parameters(locals()))

    async def add(self, schema_id: int, name: str, full_name: str):
        return await save_insert(self._client, **get_parameters(locals()))
