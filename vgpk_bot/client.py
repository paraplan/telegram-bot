from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from vgpk_bot.env import TOKEN

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
