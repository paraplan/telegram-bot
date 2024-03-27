from typing import Iterable

from aiogram import Router

from . import schedule, start

routers: Iterable[Router] = (start.router, schedule.router)
