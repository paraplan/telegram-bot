from datetime import datetime
from typing import Iterable
from zoneinfo import ZoneInfo


def datetime_filter(value: datetime) -> str:
    tz = ZoneInfo("Europe/Moscow")
    local_dt = value.astimezone(tz)
    return local_dt.strftime("%H:%M")


def datetimes_filter(datetimes: Iterable[datetime], separator: str = " - ") -> str:
    filtered_datetimes: list[str] = [datetime_filter(datetime) for datetime in datetimes]
    return separator.join(filtered_datetimes)
