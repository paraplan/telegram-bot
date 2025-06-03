from telegrinder import Dispatch, Message
from telegrinder.rules import Command
from telegrinder.types import ReplyKeyboardRemove

from src.bot.templates import render_template
from src.bot.utils.nodes import UserDB, UserSettingsDB

dp = Dispatch()


@dp.message(Command("start"))
async def handle_start(message: Message, user: UserDB, user_settings: UserSettingsDB):
    # Please, don't remove user and user_settings from arguments.
    # It's registration process.
    # For more information, please, see how these nodes are working.
    await message.answer(render_template("hello.j2"), reply_markup=ReplyKeyboardRemove(True))
