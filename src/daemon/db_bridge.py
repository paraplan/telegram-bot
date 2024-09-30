import datetime
import logging
from uuid import UUID

from src.bot.utils.notification import send_notification
from src.daemon.client import TIMEZONE, db_client
from src.database.generated import (
    InsertOrSelectSeminarResult,
    get_seminar_ids_by_date,
    insert_cabinet,
    insert_group,
    insert_or_select_seminar,
    insert_subject,
    update_or_insert_schedule,
)
from src.schedule_parser.group import Group
from src.schedule_parser.study_day import StudyDay

BellsDictType = dict[int, tuple[datetime.datetime, datetime.datetime]]
logger = logging.getLogger(__name__)


async def update_schedules(schedules: list[StudyDay]):
    bells_dict = get_bells_dict(schedules)
    for schedule in schedules:
        logger.info("Updating schedule for %s", schedule.date)
        for area in schedule.areas:
            for group in area.groups:
                seminars_for_group = await get_seminars_for_group(group, bells_dict)
                group = await insert_group(
                    db_client, full_name=group.info.full_name, name=group.info.name
                )
                if not seminars_for_group:
                    continue
                old_seminar_ids = await get_seminar_ids(group.id, schedule.date)
                await update_seminars_data(schedule.date, group.id, seminars_for_group)
                new_seminar_ids = await get_seminar_ids(group.id, schedule.date)
                if old_seminar_ids is None or old_seminar_ids != new_seminar_ids:
                    await send_notification(group, schedule.date, old_seminar_ids, new_seminar_ids)
                    logger.debug("Seminar data has changed for %s", group)
                logger.debug("Finished updating %s", group)
    logger.debug("Finished updating schedules")


async def get_seminar_ids(group_id: UUID, date: datetime.date) -> list[UUID] | None:
    seminars_data = await get_seminar_ids_by_date(db_client, group_id=group_id, date=date)
    if not seminars_data:
        return None
    return sorted([seminar.id for seminar in seminars_data.seminars])


async def update_seminars_data(
    date: datetime.date, group_id: UUID, seminars_for_group: list[InsertOrSelectSeminarResult]
):
    seminar_ids = [seminar.id for seminar in seminars_for_group]
    await update_or_insert_schedule(
        db_client,
        group_id=group_id,
        seminar_ids=seminar_ids,
        date=date,
    )


async def get_seminars_for_group(
    group: Group, bells_dict: BellsDictType
) -> list[InsertOrSelectSeminarResult]:
    seminars_for_day: list[InsertOrSelectSeminarResult] = []
    for hours_index, hours_data in group.hours.items():
        for sub_group_index, sub_group_data in hours_data.items():
            cabinet = None
            if sub_group_data.room:
                cabinet = await insert_cabinet(
                    db_client,
                    name=sub_group_data.room.full_name,
                    room=sub_group_data.room.name,
                    schema_id=sub_group_data.room.id,
                )
            subject = await insert_subject(db_client, name=sub_group_data.occupation)
            seminars_for_day.append(
                (
                    await insert_or_select_seminar(
                        db_client,
                        cabinet_schema_id=cabinet.schema_id if cabinet else None,
                        subject_name=subject.name,
                        sub_group=sub_group_index,
                        start_time=bells_dict[hours_index][0],
                        end_time=bells_dict[hours_index][1],
                        number=hours_index,
                    )
                )[0]
            )
    return seminars_for_day


def get_bells_dict(schedules: list[StudyDay]) -> BellsDictType:
    bells_dict: BellsDictType = dict()
    for schedule in schedules:
        for bell_index, bell_data in enumerate(schedule.bells.hours):
            bells_dict[bell_index] = (
                datetime.datetime.combine(schedule.date, bell_data.start, tzinfo=TIMEZONE),
                datetime.datetime.combine(schedule.date, bell_data.end, tzinfo=TIMEZONE),
            )
    return bells_dict
