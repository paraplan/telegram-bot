from zoneinfo import ZoneInfo

import edgedb
from telegrinder import (
    API,
    ABCMiddleware,
    Context,
    HTMLFormatter,
    Message,
    Telegrinder,
    Token,
    WaiterMachine,
)
from telegrinder.modules import logger
from telegrinder.types import BotCommand

from src.database.generated import InsertUserResult, insert_user
from src.env import BOT_TOKEN, LOGGER_LEVEL

TIMEZONE = ZoneInfo("Europe/Moscow")

logger.set_level(LOGGER_LEVEL)

api = API(token=Token(BOT_TOKEN))
bot = Telegrinder(api)
wm = WaiterMachine()
formatter = HTMLFormatter

db_client = edgedb.create_async_client()


@bot.on.message.register_middleware()
class UserRegisterMiddleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: Context) -> bool:
        user = await insert_user(db_client, telegram_id=event.from_user.id)
        ctx.update({"user": user})
        return True


async def update_commands():
    await api.set_my_commands(
        [
            BotCommand("start", "🤨"),
            BotCommand("group", "Выбрать группу"),
            BotCommand("tomorrow", "Расписание на завтра"),
            BotCommand("today", "Расписание на сегодня"),
        ]
    )


MiddlewareUser = InsertUserResult
