from typing import Iterable

from telegrinder import Dispatch

from . import group, schedule, schedule_callback, settings, start, subgroup

dispatches: Iterable[Dispatch] = (
    schedule_callback.dp,
    schedule.dp,
    start.dp,
    group.dp,
    subgroup.dp,
    settings.dp,
)
