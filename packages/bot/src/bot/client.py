import locale

from telegrinder import API, Dispatch, HTMLFormatter, Telegrinder, Token, WaiterMachine

from bot.utils.middlewares import AllowedUsersMiddleware
from env import BOT_TOKEN

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

api = API(token=Token(BOT_TOKEN))
dp = Dispatch()
bot = Telegrinder(api, dispatch=dp)
wm = WaiterMachine(dp)

formatter = HTMLFormatter

bot.on.message.register_middleware(AllowedUsersMiddleware)
