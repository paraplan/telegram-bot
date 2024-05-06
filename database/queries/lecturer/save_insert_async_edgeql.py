# AUTOGENERATED FROM 'database/queries/lecturer/save_insert.edgeql' WITH:
#     $ edgedb-py --dir database/queries --no-skip-pydantic-validation


from __future__ import annotations

import dataclasses
import uuid

import edgedb


@dataclasses.dataclass
class SaveInsertResult:
    id: uuid.UUID


async def save_insert(
    executor: edgedb.AsyncIOExecutor,
    *,
    schema_id: int,
    name: str,
    full_name: str,
) -> SaveInsertResult | None:
    return await executor.query_single(
        """\
        insert Lecturer {
          schema_id := <int16>$schema_id,
          name := <str>$name,
          full_name := <str>$full_name,
        } unless conflict on .schema_id;\
        """,
        schema_id=schema_id,
        name=name,
        full_name=full_name,
    )
