from datetime import date
from typing import TypedDict

from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from bot.templates import render_template

router = Router()


class Lesson(TypedDict):
    title: str
    room: str
    time: str


@router.message(Command("next_day"))
async def start(message: Message) -> None:
    lessons: list[Lesson] = []
    lessons.append({"title": "ОАиПР", "room": "3.11, 4.8", "time": "09.00 – 09.45, 09.55 – 10.40"})
    lessons.append({"title": "ТРПО", "room": "2.22", "time": "10.50 – 11.35, 11.45 – 12.30"})
    await message.answer(
        render_template("next_day.j2", {"date": date.today(), "lessons": lessons}),
        parse_mode=ParseMode.HTML,
    )
