from typing import Iterable

from telegrinder import Dispatch

from . import group, next_day, start

dispatches: Iterable[Dispatch] = (start.dp, group.dp, next_day.dp)
