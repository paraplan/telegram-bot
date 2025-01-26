import locale
from zoneinfo import ZoneInfo

from telegrinder import API, HTMLFormatter, Telegrinder, Token, WaiterMachine
from telegrinder.modules import logger

from src.bot.utils.middlewares import StageMiddleware, UserRegisterMiddleware
from src.env import BOT_TOKEN, LOGGER_LEVEL

TIMEZONE = ZoneInfo("Europe/Moscow")

logger.set_level(LOGGER_LEVEL)
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

api = API(token=Token(BOT_TOKEN))
bot = Telegrinder(api)

wm = WaiterMachine()
formatter = HTMLFormatter
db_client = ""

bot.on.message.register_middleware()(cls=StageMiddleware)
bot.on.message.register_middleware()(cls=UserRegisterMiddleware)
