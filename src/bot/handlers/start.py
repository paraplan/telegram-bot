from telegrinder import Dispatch, Message
from telegrinder.rules import Command
from telegrinder.types import ReplyKeyboardRemove

from src.bot.templates import render_template

dp = Dispatch()


@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer(render_template("hello.j2"), reply_markup=ReplyKeyboardRemove(True))
