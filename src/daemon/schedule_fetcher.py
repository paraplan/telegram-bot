import datetime
import logging

import orjson

from src.daemon.http_client import FetchError, get_schedule_data
from src.schedule_parser.study_day import StudyDay

logger = logging.getLogger(__name__)


async def get_updated_schedules() -> list[StudyDay]:
    updated_schedules: list[StudyDay] = []

    dates = get_dates_for_fetch()
    for date in dates:
        try:
            schedule_data = await get_schedule_data(date)
            updated_schedules.append(StudyDay(**orjson.loads(schedule_data)))
        except FetchError as e:
            logger.error("Failed to fetch schedule data for %s: %s", date, e)
    return updated_schedules


def get_dates_for_fetch() -> list[datetime.date]:
    today = datetime.date.today()
    dates: list[datetime.date] = [today]
    if today.weekday() == 4:  # Friday
        dates += [today + datetime.timedelta(days=1), today + datetime.timedelta(days=3)]
    elif today.weekday() == 5:  # Saturday
        dates.append(today + datetime.timedelta(days=2))
    elif today.weekday() == 6:  # Sunday
        dates = [today + datetime.timedelta(days=1)]
    else:  # Monday - Thursday
        dates.append(today + datetime.timedelta(days=1))
    logger.debug("Dates for fetch: %s", dates)
    return dates
