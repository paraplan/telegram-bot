import locale
import logging

from telegrinder import API, Dispatch, Telegrinder, Token, setup_logger
from telegrinder.tools.formatting import HTML

from src.bot.utils.middlewares import AllowedUsersMiddleware
from src.env import BOT_TOKEN

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

setup_logger(module="logging", console_sink=None)
logging.getLogger("telegrinder").setLevel(logging.NOTSET)

api = API(token=Token(BOT_TOKEN))
dp = Dispatch()
bot = Telegrinder(api, dispatch=dp)

formatter = HTML

bot.on.message.register_middleware(AllowedUsersMiddleware)
