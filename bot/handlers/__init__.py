from typing import Iterable

from aiogram import Router

from . import start

routers: Iterable[Router] = (start.router,)
