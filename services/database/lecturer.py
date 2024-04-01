from typing import Final

from . import SingletonClient, get_parameters, read_query_file

INSERT: Final[str] = read_query_file("lecturer/unconflict_insert.edgeql")
SELECT_BY_SCHEMA_ID: Final[str] = read_query_file("lecturer/select_by_schema_id.edgeql")


class LecturerRepository:
    def __init__(self) -> None:
        self._client = SingletonClient.get_instance()

    async def get_by_id(self, schema_id: int) -> list[object]:
        return await self._client.query(SELECT_BY_SCHEMA_ID, schema_id=schema_id)

    async def add(self, schema_id: int, name: str, full_name: str) -> None:
        return await self._client.execute(INSERT, **get_parameters(locals()))
