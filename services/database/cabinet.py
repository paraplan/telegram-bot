from database.queries.cabinet import save_insert, select_by_schema_id

from . import BaseRepository, get_parameters


class CabinetRepository(BaseRepository):
    async def get_by_id(self, schema_id: int):
        return await select_by_schema_id(self._client, **get_parameters(locals()))

    async def add(self, number: str, schema_id: int, title: str):
        return await save_insert(self._client, **get_parameters(locals()))
