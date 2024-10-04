from typing import Iterable

from telegrinder import Dispatch

from . import group, schedule, start, subgroup

dispatches: Iterable[Dispatch] = (start.dp, group.dp, schedule.dp, subgroup.dp)
