from datetime import datetime
from zoneinfo import ZoneInfo


def datetime_filter(value: datetime) -> str:
    tz = ZoneInfo("Europe/Moscow")
    local_dt = value.astimezone(tz)
    return local_dt.strftime("%H:%M")
