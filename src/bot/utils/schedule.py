import dataclasses
import datetime
from typing import Iterable

from telegrinder import InlineButton, InlineKeyboard
from telegrinder.types import InlineKeyboardMarkup

from src.bot.templates import render_template
from src.bot.utils.seminars import convert_schedule_to_pairs
from src.database import RepositoryFactory
from src.database.models import Group


@dataclasses.dataclass(slots=True, frozen=True)
class ScheduleCallbackData:
    date: str  # TODO: datetime.date now is not supported by telegrinder
    group_id: int
    subgroup: int


async def render_schedule_for_date(
    repository: RepositoryFactory,
    date: datetime.date,
    group: Group | None = None,
    sub_group: int = 1,
) -> tuple[str, InlineKeyboardMarkup]:
    kb = InlineKeyboard()
    if not group:
        return "Вы не выбрали группу. Чтобы сделать это, введите /group", kb.get_markup()
    schedule = await repository.group.get_schedule(group.id, date)
    if not schedule:
        return (
            f"Расписания {group.name} на {date.strftime('%d.%m.%Y')} не найдено",
            kb.get_markup(),
        )
    schedule = sorted(schedule, key=lambda x: x.time_slot.lesson_number)
    grouped_seminars, _ = convert_schedule_to_pairs(schedule, sub_group)
    is_schedule_subgrouped = len(set((item.subgroup for item in schedule))) > 1
    if is_schedule_subgrouped:
        kb = _get_subgroups_keyboard(group.id, date, sub_group)
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
    group_id: int, date: datetime.date, selected_subgroup: int, subgroups: Iterable[int] = (1, 2)
) -> InlineKeyboard:
    kb = InlineKeyboard()
    for subgroup in subgroups:
        text = (
            f"*{subgroup} подгруппа*" if subgroup == selected_subgroup else f"{subgroup} подгруппа"
        )
        data = ScheduleCallbackData(
            subgroup=subgroup, date=date.strftime("%Y-%m-%d"), group_id=group_id
        )
        kb.add(InlineButton(text, callback_data=data))
    return kb
