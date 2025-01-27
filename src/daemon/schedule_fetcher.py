import datetime

import orjson
from loguru import logger

from src.daemon.http_client import FetchError, get_schedule_data
from src.schedule_parser.study_day import StudyDaySchema


async def get_updated_schedules() -> list[StudyDaySchema]:
    updated_schedules: list[StudyDaySchema] = []

    dates = get_dates_for_fetch()
    for date in dates:
        try:
            schedule_data = await get_schedule_data(date)
            updated_schedules.append(StudyDaySchema(**orjson.loads(schedule_data)))
        except FetchError as e:
            logger.error(f"Failed to fetch schedule data for {date}: {e}")
    return updated_schedules


def get_dates_for_fetch() -> list[datetime.date]:
    today = datetime.date.today()
    dates: list[datetime.date] = []
    if today.weekday() == 4:  # Friday
        dates += [today + datetime.timedelta(days=1), today + datetime.timedelta(days=3)]
    elif today.weekday() == 5:  # Saturday
        dates.append(today + datetime.timedelta(days=2))
    elif today.weekday() == 6:  # Sunday
        dates = [today + datetime.timedelta(days=1)]
    else:  # Monday - Thursday
        dates.append(today + datetime.timedelta(days=1))
    logger.debug(f"Dates for fetch: {dates}")
    return dates
