from typing import Final

from . import SingletonClient, get_parameters, read_query_file

INSERT: Final[str] = read_query_file("cabinet/unconflict_insert.edgeql")
SELECT_BY_SCHEMA_ID: Final[str] = read_query_file("cabinet/select_by_schema_id.edgeql")


class CabinetRepository:
    def __init__(self) -> None:
        self._client = SingletonClient.get_instance()

    async def get_by_id(self, schema_id: int) -> list[object]:
        return await self._client.query(SELECT_BY_SCHEMA_ID, schema_id=schema_id)

    async def add(self, number: str, schema_id: int, title: str) -> None:
        return await self._client.execute(INSERT, **get_parameters(locals()))
