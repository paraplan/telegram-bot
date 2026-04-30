import locale

from telegrinder import API, Dispatch, Telegrinder, Token
from telegrinder.tools.formatting import HTML

from src.bot.utils.middlewares import AllowedUsersMiddleware
from src.env import BOT_TOKEN

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

api = API(token=Token(BOT_TOKEN))
dp = Dispatch()
bot = Telegrinder(api, dispatch=dp)

formatter = HTML

bot.on.message.register_middleware(AllowedUsersMiddleware)
