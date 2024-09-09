# AUTOGENERATED FROM:
#     'src/database/queries/cabinets/insert_cabinet.edgeql'
#     'src/database/queries/groups/insert_group.edgeql'
#     'src/database/queries/seminars/insert_or_select_seminar.edgeql'
#     'src/database/queries/subject/insert_subject.edgeql'
#     'src/database/queries/schedule/select_schedule.edgeql'
#     'src/database/queries/to_json.edgeql'
#     'src/database/queries/schedule/update_or_insert_schedule.edgeql'
# WITH:
#     $ edgedb-py --dir src/database/queries --target async --file src/database/generated.py


from __future__ import annotations

import dataclasses
import datetime
import uuid

import edgedb


class NoPydanticValidation:
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        # Pydantic 2.x
        from pydantic_core.core_schema import any_schema

        return any_schema()


@dataclasses.dataclass
class InsertCabinetResult(NoPydanticValidation):
    id: uuid.UUID
    name: str
    room: str
    schema_id: int


@dataclasses.dataclass
class InsertGroupResult(NoPydanticValidation):
    id: uuid.UUID
    full_name: str
    name: str


@dataclasses.dataclass
class InsertOrSelectSeminarResult(NoPydanticValidation):
    id: uuid.UUID
    end_time: datetime.datetime
    number: int
    start_time: datetime.datetime
    sub_group: int
    cabinet: InsertCabinetResult | None
    subject: InsertOrSelectSeminarResultSubject


@dataclasses.dataclass
class InsertOrSelectSeminarResultSubject(NoPydanticValidation):
    id: uuid.UUID
    name: str


@dataclasses.dataclass
class SelectScheduleResult(NoPydanticValidation):
    id: uuid.UUID
    date: datetime.datetime
    group: InsertGroupResult
    seminars: list[SelectScheduleResultSeminarsItem]


@dataclasses.dataclass
class SelectScheduleResultSeminarsItem(NoPydanticValidation):
    id: uuid.UUID
    end_time: datetime.datetime
    number: int
    start_time: datetime.datetime
    sub_group: int


async def insert_cabinet(
    executor: edgedb.AsyncIOExecutor,
    *,
    name: str,
    room: str,
    schema_id: int,
) -> InsertCabinetResult:
    return await executor.query_single(
        """\
        with
          cabinet := (
            insert Cabinet {
              name := <str>$name,
              room := <str>$room,
              schema_id := <int32>$schema_id
            } unless conflict on .schema_id else Cabinet
          )

        select cabinet {**};\
        """,
        name=name,
        room=room,
        schema_id=schema_id,
    )


async def insert_group(
    executor: edgedb.AsyncIOExecutor,
    *,
    full_name: str,
    name: str,
) -> InsertGroupResult:
    return await executor.query_single(
        """\
        select (
          insert `Group` {
            full_name := <str>$full_name,
            name := <str>$name
          } unless conflict on .full_name else `Group`
        ) {*};\
        """,
        full_name=full_name,
        name=name,
    )


async def insert_or_select_seminar(
    executor: edgedb.AsyncIOExecutor,
    *,
    cabinet_schema_id: int | None = None,
    subject_name: str,
    sub_group: int,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    number: int,
) -> list[InsertOrSelectSeminarResult]:
    return await executor.query(
        """\
        WITH
          cabinet := (
            SELECT Cabinet
            FILTER .schema_id = <optional int32>$cabinet_schema_id
          ),
          subject := (
            SELECT Subject
            FILTER .name = <str>$subject_name
          ),
          seminar := (
            SELECT Seminar
            FILTER
              .cabinet = cabinet AND
              .subject = subject AND
              .sub_group = <int16>$sub_group AND
              .start_time = <datetime>$start_time AND
              .end_time = <datetime>$end_time AND
              .number = <int16>$number
          )

        SELECT (
          IF EXISTS seminar THEN
            seminar
          ELSE (
            INSERT Seminar {
              cabinet := cabinet,
              subject := subject,
              sub_group := <int16>$sub_group,
              start_time := <datetime>$start_time,
              end_time := <datetime>$end_time,
              number := <int16>$number,
            }
          )
        ) { ** };\
        """,
        cabinet_schema_id=cabinet_schema_id,
        subject_name=subject_name,
        sub_group=sub_group,
        start_time=start_time,
        end_time=end_time,
        number=number,
    )


async def insert_subject(
    executor: edgedb.AsyncIOExecutor,
    *,
    name: str,
) -> InsertOrSelectSeminarResultSubject:
    return await executor.query_single(
        """\
        with
          subject := (
            insert Subject {
              name := <str>$name,
            } unless conflict on .name else Subject
          )

        select subject {**};\
        """,
        name=name,
    )


async def select_schedule(
    executor: edgedb.AsyncIOExecutor,
    *,
    group_id: uuid.UUID,
    seminar_ids: list[uuid.UUID],
    date: datetime.datetime,
) -> list[SelectScheduleResult]:
    return await executor.query(
        """\
        WITH
          `group` := (
            SELECT `Group`
            FILTER .id = <uuid>$group_id
          ),
          seminars := (
            SELECT Seminar
            FILTER .id = array_unpack(<array<uuid>>$seminar_ids)
          ),
          schedule := (
            SELECT SeminarSchedule
            FILTER
              .`group` = `group` AND
              .seminars = seminars AND
              .date = <datetime>$date
          )

        SELECT (
          schedule
        ) { ** };\
        """,
        group_id=group_id,
        seminar_ids=seminar_ids,
        date=date,
    )


async def to_json(
    executor: edgedb.AsyncIOExecutor,
    *,
    string: str,
) -> str:
    return await executor.query_single(
        """\
        select to_json(<str>$string);\
        """,
        string=string,
    )


async def update_or_insert_schedule(
    executor: edgedb.AsyncIOExecutor,
    *,
    group_id: uuid.UUID,
    seminar_ids: list[uuid.UUID],
    date: datetime.datetime,
) -> list[SelectScheduleResult]:
    return await executor.query(
        """\
        WITH
          group_obj := (
            SELECT `Group`
            FILTER .id = <uuid>$group_id
          ),
          seminars := (
            SELECT Seminar
            FILTER .id IN array_unpack(<array<uuid>>$seminar_ids)
          ),
          schedule := (
            SELECT SeminarSchedule
            FILTER
              .`group` = group_obj AND
              .date = <datetime>$date
          )

        SELECT (
          IF EXISTS schedule THEN
            (
              UPDATE SeminarSchedule
              FILTER .id = schedule.id
              SET {
                seminars := seminars,
              }
            )
          ELSE (
            INSERT SeminarSchedule {
              `group` := group_obj,
              seminars := seminars,
              date := <datetime>$date,
            }
          )
        ) { ** };\
        """,
        group_id=group_id,
        seminar_ids=seminar_ids,
        date=date,
    )
