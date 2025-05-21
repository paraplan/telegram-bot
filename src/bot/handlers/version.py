from telegrinder import Dispatch, Message
from telegrinder.rules import Command
from telegrinder.types import LinkPreviewOptions

from src.bot.templates import render_template

dp = Dispatch()


@dp.message(Command("version"))
async def version(message: Message):
    await message.answer(
        render_template("version.j2"),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
