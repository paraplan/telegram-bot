import datetime
from typing import Iterable
from zoneinfo import ZoneInfo


def datetime_filter(date: datetime.datetime) -> str:
    tz = ZoneInfo("Europe/Moscow")
    date = date.astimezone(tz)
    return date.strftime("%H:%M")


def datetimes_filter(datetimes: Iterable[datetime.datetime], separator: str = " - ") -> str:
    filtered_datetimes: list[str] = [datetime_filter(datetime) for datetime in datetimes]
    return separator.join(filtered_datetimes)
