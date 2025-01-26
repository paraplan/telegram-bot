from typing import Iterable

from telegrinder import Dispatch

from . import group, schedule, schedule_callback, start, subgroup

dispatches: Iterable[Dispatch] = (
    start.dp,
    group.dp,
    schedule.dp,
    subgroup.dp,
    schedule_callback.dp,
)
