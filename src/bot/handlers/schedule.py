import datetime

from telegrinder import (
    CALLBACK_QUERY_FOR_MESSAGE,
    MESSAGE_FROM_USER,
    CallbackQueryCute,
    Dispatch,
    InlineButton,
    InlineKeyboard,
    Message,
    MessageCute,
)
from telegrinder.rules import CallbackDataEq, Command, Regex

from src.bot.client import formatter, wm
from src.bot.utils.schedule import render_schedule_for_date
from src.database import RepositoryFactory
from src.database.models import User, UserSettings

dp = Dispatch()


@dp.message(Command("tomorrow"))
async def handle_tomorrow(
    message: Message, user: User, user_settings: UserSettings, repository: RepositoryFactory
):
    text, keyboard = await render_schedule_for_date(
        repository, message.date + datetime.timedelta(days=1), user.group, user_settings.subgroup
    )
    resp = await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)
    resp.unwrap()


@dp.message(Command("today"))
async def handle_today(
    message: Message, user: User, user_settings: UserSettings, repository: RepositoryFactory
):
    text, keyboard = await render_schedule_for_date(
        repository, message.date, user.group, user_settings.subgroup
    )
    await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)


@dp.message(Command("monday"))
async def handle_monday(
    message: Message, user: User, user_settings: UserSettings, repository: RepositoryFactory
):
    message_weekday = message.date.weekday()
    days_ahead = 7 - message_weekday
    if days_ahead == 7:
        days_ahead = 0
    text, keyboard = await render_schedule_for_date(
        repository,
        message.date + datetime.timedelta(days=days_ahead),
        user.group,
        user_settings.subgroup,
    )
    await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)


@dp.message(Command("week"))
async def handle_week(
    message: Message, user: User, user_settings: UserSettings, repository: RepositoryFactory
):
    text, keyboard = await render_schedule_for_date(
        repository, message.date, user.group, user_settings.subgroup, is_week=True
    )
    await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)


DATE_KEYBOARD = InlineKeyboard()
DATE_KEYBOARD.add(InlineButton("Расписание на сегодня", callback_data="today"))
DATE_KEYBOARD.add(InlineButton("Расписание на завтра", callback_data="tomorrow"))
DATE_KEYBOARD.row()
DATE_KEYBOARD.add(InlineButton("Отменить ввод даты", callback_data="cancel"))


@dp.message(Command("date"))
async def handle_date(
    message: Message, user: User, user_settings: UserSettings, repository: RepositoryFactory
):
    request_message = await message.answer(
        "Напишите дату в формате DD.MM.YYYY или выберите дату из списка",
        reply_markup=DATE_KEYBOARD.get_markup(),
    )
    request_message_id = request_message.unwrap().message_id

    _, event, _ = await wm.wait_many(
        MESSAGE_FROM_USER(message.from_user.id),
        CALLBACK_QUERY_FOR_MESSAGE(request_message_id),
        release=Regex(r"\d{2}\.\d{2}\.\d{4}")
        | CallbackDataEq("cancel")
        | CallbackDataEq("today")
        | CallbackDataEq("tomorrow"),
    )

    date: datetime.datetime
    match event:
        case MessageCute():
            date = datetime.datetime.strptime(event.text.unwrap(), "%d.%m.%Y")
        case CallbackQueryCute():
            callback_data = event.data.unwrap()
            if callback_data == "today":
                date = message.date
            elif callback_data == "tomorrow":
                date = message.date + datetime.timedelta(days=1)
            else:
                return

    text, keyboard = await render_schedule_for_date(
        repository, date, user.group, user_settings.subgroup, is_week=True
    )
    await message.ctx_api.edit_message_text(
        chat_id=message.chat_id,
        message_id=request_message_id,
        text=text,
        parse_mode=formatter.PARSE_MODE,
        reply_markup=keyboard,
    )


@dp.message(Command("next"))
async def handle_next(
    message: Message, user: User, user_settings: UserSettings, repository: RepositoryFactory
):
    if user.group is None:
        await message.answer("Вы не выбрали группу. Чтобы сделать это, введите /group")
        return
    date = await repository.schedule.select_nearest_date_with_schedule(user.group.id)
    if date is None:
        await message.answer(
            "📚 Расписание на ближайшие дни не найдено, попробуйте команды /tomorrow или /today"
        )
        return
    text, keyboard = await render_schedule_for_date(
        repository, date, user.group, user_settings.subgroup, is_week=False
    )
    await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)
