# AUTOGENERATED FROM 'database/queries/cabinet/save_insert.edgeql' WITH:
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
    number: str,
    schema_id: int,
    title: str,
) -> SaveInsertResult | None:
    return await executor.query_single(
        """\
        insert Cabinet {
          number := <str>$number,
          schema_id := <int16>$schema_id,
          title := <str>$title,
        } unless conflict on .schema_id;\
        """,
        number=number,
        schema_id=schema_id,
        title=title,
    )
