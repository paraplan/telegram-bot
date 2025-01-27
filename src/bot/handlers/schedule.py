import datetime

from telegrinder import MESSAGE_FROM_USER, Dispatch, Message, MessageReplyHandler
from telegrinder.rules import Command, Regex

from src.bot.client import formatter, wm
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


@dp.message(Command("date"))
async def handle_date(message: Message, user: User, repository: RepositoryFactory):
    await message.answer("Напишите дату в формате DD.MM.YYYY")
    message, _ = await wm.wait(
        MESSAGE_FROM_USER,
        message.from_user.id,
        release=Regex(r"\d{2}\.\d{2}\.\d{4}"),
        on_miss=MessageReplyHandler("Вы ввели некорректную дату", as_reply=True),
    )
    date = datetime.datetime.strptime(message.text.unwrap(), "%d.%m.%Y")
    text, keyboard = await render_schedule_for_date(
        repository, date, user.group, user.settings.subgroup, is_week=True
    )
    await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)
