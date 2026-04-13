from telegrinder import Dispatch, Message
from telegrinder.rules import Command
from telegrinder.types import ReplyKeyboardRemove

from src.bot.templates import render_template
from src.bot.utils.nodes import DBRepository

dp = Dispatch()


@dp.message(Command("start"))
async def handle_start(message: Message, database: DBRepository):
    user = await database.user.select_or_insert(message.from_user.id)
    await database.user_settings.select_or_insert(user.id)
    await message.answer(render_template("hello.j2"), reply_markup=ReplyKeyboardRemove(True))
