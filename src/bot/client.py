import locale
from zoneinfo import ZoneInfo

from telegrinder import API, Dispatch, HTMLFormatter, Telegrinder, Token, WaiterMachine
from telegrinder.modules import logger

from src.bot.utils.middlewares import StageMiddleware, UserRegisterMiddleware
from src.env import BOT_TOKEN, LOGGER_LEVEL

TIMEZONE = ZoneInfo("Europe/Moscow")

logger.set_level(LOGGER_LEVEL)
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

api = API(token=Token(BOT_TOKEN))
dp = Dispatch()
bot = Telegrinder(api, dispatch=dp)
wm = WaiterMachine(dp)

formatter = HTMLFormatter

bot.on.message.register_middleware()(cls=StageMiddleware)
bot.on.message.register_middleware()(cls=UserRegisterMiddleware)
