from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.templates import render_template

router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        render_template(
            "hello.j2", {"name": message.from_user.first_name if message.from_user else None}
        ),
        parse_mode=ParseMode.HTML,
    )
