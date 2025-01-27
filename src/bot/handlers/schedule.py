import datetime

from telegrinder import Dispatch, Message
from telegrinder.rules import Command

from src.bot.client import formatter
from src.bot.utils.schedule import render_schedule_for_date
from src.database import RepositoryFactory
from src.database.models import User

dp = Dispatch()


@dp.message(Command("tomorrow"))
async def handle_tomorrow(message: Message, user: User, repository: RepositoryFactory):
    text, keyboard = await render_schedule_for_date(
        repository, message.date + datetime.timedelta(days=1), user.group, user.settings.subgroup
    )
    resp = await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)
    resp.unwrap()


@dp.message(Command("today"))
async def handle_today(message: Message, user: User, repository: RepositoryFactory):
    text, keyboard = await render_schedule_for_date(
        repository, message.date, user.group, user.settings.subgroup
    )
    await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)


@dp.message(Command("monday"))
async def handle_monday(message: Message, user: User, repository: RepositoryFactory):
    message_weekday = message.date.weekday()
    days_ahead = 7 - message_weekday
    if days_ahead == 7:
        days_ahead = 0
    text, keyboard = await render_schedule_for_date(
        repository,
        message.date + datetime.timedelta(days=days_ahead),
        user.group,
        user.settings.subgroup,
    )
    await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)


@dp.message(Command("week"))
async def handle_week(message: Message, user: User, repository: RepositoryFactory):
    text, keyboard = await render_schedule_for_date(
        repository, message.date, user.group, user.settings.subgroup, is_week=True
    )
    await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)
