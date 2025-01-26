import datetime
import logging

from src.daemon.group_bridge import process_group
from src.database import DayTypeCreate, RepositoryFactory, TimeSlotCreate
from src.schedule_parser.area import AreaSchema
from src.schedule_parser.base import BaseItemSchema
from src.schedule_parser.bells import BellsHoursSchema
from src.schedule_parser.study_day import StudyDaySchema


async def update_schedules(schedules: list[StudyDaySchema]) -> None:
    repository = RepositoryFactory()
    for schedule in schedules:
        logging.info("Updating schedule for %s", schedule.date)
        day_type = await process_day_type(repository, schedule.bells.info)
        time_slot_ids = await process_time_slot(repository, schedule.bells.hours, day_type.id)
        for area in schedule.areas:
            await process_area(repository, area, schedule.date, time_slot_ids)


async def process_day_type(
    repository: RepositoryFactory, bells_info: BaseItemSchema
) -> DayTypeCreate:
    day_type_create = DayTypeCreate(id=bells_info.id, name=bells_info.name)
    logging.debug("Processed day type: %s", day_type_create)
    await repository.day_type.insert(day_type_create)
    return day_type_create


async def process_time_slot(
    repository: RepositoryFactory, bells: list[BellsHoursSchema], day_type_id: int
) -> dict[int, int]:
    result: dict[int, int] = dict()
    for index, bell in enumerate(bells):
        time_slot_create = TimeSlotCreate(
            day_type_id=day_type_id,
            start_time=bell.start,
            end_time=bell.end,
            lesson_number=index,
        )
        time_slot = await repository.time_slot.insert_or_select(time_slot_create)
        result[index] = time_slot.id
    logging.debug("Processed time slots: %s", result)
    return result


async def process_area(
    repository: RepositoryFactory,
    area: AreaSchema,
    schedule_date: datetime.date,
    time_slot_ids: dict[int, int],
) -> None:
    for group in area.groups:
        logging.debug("Processing group %s", group.info.full_name)
        await process_group(repository, group, schedule_date, time_slot_ids)
