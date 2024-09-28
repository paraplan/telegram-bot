import locale
from zoneinfo import ZoneInfo

import edgedb
from telegrinder import API, HTMLFormatter, Telegrinder, Token, WaiterMachine
from telegrinder.modules import logger
from telegrinder.types import BotCommand

from src.env import BOT_TOKEN, EDGEDB_DSN, LOGGER_LEVEL

TIMEZONE = ZoneInfo("Europe/Moscow")

logger.set_level(LOGGER_LEVEL)
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

api = API(token=Token(BOT_TOKEN))
bot = Telegrinder(api)
wm = WaiterMachine()
formatter = HTMLFormatter

db_client = edgedb.create_async_client(EDGEDB_DSN, tls_security="insecure")


async def update_commands():
    await api.set_my_commands(
        [
            BotCommand("start", "🤨"),
            BotCommand("group", "Выбрать группу"),
            BotCommand("tomorrow", "Расписание на завтра"),
            BotCommand("today", "Расписание на сегодня"),
            BotCommand("monday", "Расписание на понедельник"),
        ]
    )
