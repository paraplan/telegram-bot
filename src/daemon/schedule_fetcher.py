import datetime

import orjson
from loguru import logger

from src.daemon.http_client import FetchError, get_schedule_data
from src.schedule_parser.study_day import StudyDaySchema


async def get_schedules_for_updating() -> list[StudyDaySchema]:
    schedules_for_updating: list[StudyDaySchema] = []

    n = 1
    max_n = 5
    while n <= max_n:
        day = get_business_day_with_delta(n)
        try:
            schedule_data = await get_schedule_data(day)
        except FetchError as e:
            logger.error(f"Failed to fetch schedule data for {day}: {e}")
            n += 1
            continue
        schedule = StudyDaySchema(**orjson.loads(schedule_data))
        schedules_for_updating.append(schedule)
        if schedule.date.weekday() == 6:  # for addition parsing of Monday schedule
            n += 1
            continue
        break

    logger.debug(f"Found {len(schedules_for_updating)} schedules for updating")
    return schedules_for_updating


def get_business_day_with_delta(days_delta: int) -> datetime.date:
    """Returns the next business day with a given delta. Includes saturdays."""
    today = datetime.date.today()
    if today.weekday() == 6:  # 6 == Sunday
        if days_delta >= 0:
            today += datetime.timedelta(days=1)
        else:
            today -= datetime.timedelta(days=1)

    # move in the right direction
    step = 1 if days_delta >= 0 else -1
    remaining = days_delta

    # move in the right direction, skipping weekends
    while remaining != 0:
        today += datetime.timedelta(days=step)
        if today.weekday() != 6:
            remaining -= step

    return today
