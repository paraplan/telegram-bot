import dataclasses
import datetime
from typing import Iterable

from telegrinder import CallbackQuery, Dispatch, InlineButton, InlineKeyboard, Message
from telegrinder.rules import CallbackDataJsonModel, Command
from telegrinder.types import InlineKeyboardMarkup

from src.bot.client import db_client, formatter
from src.bot.templates import render_template
from src.bot.utils.middlewares import MiddlewareType
from src.bot.utils.seminars import convert_schedule_to_pairs
from src.database.generated import GetAllGroupsResult, get_group_by_name, get_schedule_by_group

dp = Dispatch()


@dataclasses.dataclass(slots=True, frozen=True)
class ScheduleCallbackData:
    date: str  # TODO: datetime.date now is not supported by telegrinder
    group_name: str
    subgroup: int


@dp.callback_query(CallbackDataJsonModel(ScheduleCallbackData, alias="data"))
async def handle_subgroup(callback: CallbackQuery, data: ScheduleCallbackData):
    date = datetime.datetime.strptime(data.date, "%Y-%m-%d").date()
    group = await get_group_by_name(db_client, group_name=data.group_name)
    text, keyboard = await _render_schedule_for_date(date, group, data.subgroup)
    await callback.edit_text(text=text, reply_markup=keyboard, parse_mode=formatter.PARSE_MODE)


@dp.message(Command("tomorrow"))
async def handle_tomorrow(message: Message, user: MiddlewareType):
    text, keyboard = await _render_schedule_for_date(
        message.date + datetime.timedelta(days=1), user.group
    )
    resp = await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)
    resp.unwrap()


@dp.message(Command("today"))
async def handle_today(message: Message, user: MiddlewareType):
    text, keyboard = await _render_schedule_for_date(message.date, user.group)
    await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)


@dp.message(Command("monday"))
async def handle_monday(message: Message, user: MiddlewareType):
    message_weekday = message.date.weekday()
    days_ahead = 7 - message_weekday
    if days_ahead == 7:
        days_ahead = 0
    text, keyboard = await _render_schedule_for_date(
        message.date + datetime.timedelta(days=days_ahead), user.group
    )
    await message.answer(text, parse_mode=formatter.PARSE_MODE, reply_markup=keyboard)


async def _render_schedule_for_date(
    date: datetime.date, group: GetAllGroupsResult | None = None, sub_group: int = 1
) -> tuple[str, InlineKeyboardMarkup]:
    kb = InlineKeyboard()
    if not group:
        return "Вы не выбрали группу. Чтобы сделать это, введите /group", kb.get_markup()
    schedule = await get_schedule_by_group(db_client, group_id=group.id, date=date)
    if not schedule:
        return (
            f"Расписания {group.name} на {date.strftime('%d.%m.%Y')} не найдено",
            kb.get_markup(),
        )
    grouped_seminars, is_schedule_subgrouped = convert_schedule_to_pairs(
        schedule.seminars, sub_group
    )
    if is_schedule_subgrouped:
        kb = _get_subgroups_keyboard(group.name, date, sub_group)
    return render_template(
        "schedule.j2",
        {
            "grouped_seminars": grouped_seminars,
            "date": date,
            "group": group,
            "sub_group": sub_group if is_schedule_subgrouped else 0,
        },
    ), kb.get_markup()


def _get_subgroups_keyboard(
    group_name: str, date: datetime.date, selected_subgroup: int, subgroups: Iterable[int] = (1, 2)
) -> InlineKeyboard:
    kb = InlineKeyboard()
    for subgroup in subgroups:
        text = (
            f"*{subgroup} подгруппа*" if subgroup == selected_subgroup else f"{subgroup} подгруппа"
        )
        data = ScheduleCallbackData(
            subgroup=subgroup, date=date.strftime("%Y-%m-%d"), group_name=group_name
        )
        kb.add(InlineButton(text, callback_data=data))
    return kb
