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

from src.bot.client import formatter
from src.bot.utils.nodes import DBRepository, UserDB, UserSettingsDB
from src.bot.utils.schedule import render_schedule_for_date

dp = Dispatch()


@dp.message(Command("tomorrow"))
async def handle_tomorrow(
    message: Message, user: UserDB, user_settings: UserSettingsDB, repository: DBRepository
):
    text, keyboard = await render_schedule_for_date(
        repository, message.date + datetime.timedelta(days=1), user.group, user_settings.subgroup
    )
    resp = await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)
    resp.unwrap()


@dp.message(Command("today"))
async def handle_today(
    message: Message, user: UserDB, user_settings: UserSettingsDB, repository: DBRepository
):
    text, keyboard = await render_schedule_for_date(
        repository, message.date, user.group, user_settings.subgroup
    )
    await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)


@dp.message(Command("monday"))
async def handle_monday(
    message: Message, user: UserDB, user_settings: UserSettingsDB, repository: DBRepository
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
    message: Message, user: UserDB, user_settings: UserSettingsDB, repository: DBRepository
):
    text, keyboard = await render_schedule_for_date(
        repository, message.date, user.group, user_settings.subgroup, is_week=True
    )
    await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)


DATE_KEYBOARD = InlineKeyboard()
DATE_KEYBOARD.add(InlineButton("На сегодня", callback_data="today"))
DATE_KEYBOARD.add(InlineButton("На завтра", callback_data="tomorrow"))
DATE_KEYBOARD.row()
DATE_KEYBOARD.add(InlineButton("Отменить ввод даты", callback_data="cancel"))


@dp.message(Command("date"))
async def handle_date(
    message: Message, user: UserDB, user_settings: UserSettingsDB, repository: DBRepository
):
    request_message = (
        await message.answer(
            "🗓️ Напишите дату в формате DD.MM.YYYY или выберите дату из списка",
            reply_markup=DATE_KEYBOARD.get_markup(),
        )
    ).unwrap()

    _, event, _ = await dp.wait_many(
        MESSAGE_FROM_USER(message.from_user.id),
        CALLBACK_QUERY_FOR_MESSAGE(request_message.message_id),
        release=Regex(r"\d{2}\.\d{2}\.\d{4}") | CallbackDataEq(["cancel", "today", "tomorrow"]),
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
                await message.api.edit_message_text(
                    chat_id=message.chat_id,
                    message_id=request_message.message_id,
                    text="ℹ️ Ввод даты отменен",
                )
                return

    text, keyboard = await render_schedule_for_date(
        repository, date, user.group, user_settings.subgroup, is_week=True
    )
    await message.api.edit_message_text(
        chat_id=message.chat_id,
        message_id=request_message.message_id,
        text=text,
        parse_mode=formatter.PARSE_MODE,
        reply_markup=keyboard,
    )


@dp.message(Command("next"))
async def handle_next(
    message: Message, user: UserDB, user_settings: UserSettingsDB, repository: DBRepository
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
