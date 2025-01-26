import datetime
from typing import Iterable


def datetime_filter(date: datetime.datetime | datetime.time) -> str:
    return date.strftime("%H:%M")


def datetimes_filter(
    datetimes: Iterable[datetime.datetime | datetime.time], separator: str = " - "
) -> str:
    filtered_datetimes: list[str] = [datetime_filter(datetime) for datetime in datetimes]
    return separator.join(filtered_datetimes)
