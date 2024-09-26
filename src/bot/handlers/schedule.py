import datetime

from telegrinder import Dispatch, Message
from telegrinder.rules import Command

from src.bot.client import MiddlewareUser, db_client, formatter
from src.bot.templates import render_template
from src.bot.utils.seminars import group_seminars_for_numbers
from src.database.generated import GetAllGroupsResult, get_schedule_by_group

dp = Dispatch()


@dp.message(Command("tomorrow"))
async def handle_tomorrow(message: Message, user: MiddlewareUser):
    schedule = await _render_schedule_for_date(
        message.date + datetime.timedelta(days=1), user.group
    )
    await message.answer(schedule, parse_mode=formatter.PARSE_MODE)


@dp.message(Command("today"))
async def handle_today(message: Message, user: MiddlewareUser):
    schedule = await _render_schedule_for_date(message.date, user.group)
    await message.answer(schedule, parse_mode=formatter.PARSE_MODE)


async def _render_schedule_for_date(
    date: datetime.date, group: GetAllGroupsResult | None = None
) -> str:
    if not group:
        return "Вы не выбрали группу. Чтобы сделать это, введите /group"
    schedule = await get_schedule_by_group(db_client, group_id=group.id, date=date)
    if not schedule:
        return f"Расписания на {date.strftime('%d.%m.%Y')} не найдено"
    grouped_seminars = group_seminars_for_numbers(schedule.seminars)
    return render_template(
        "schedule.j2",
        {"grouped_seminars": grouped_seminars, "date": date, "group": group},
    )