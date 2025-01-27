import dataclasses
import datetime
from typing import Iterable

from telegrinder import InlineButton, InlineKeyboard, RowButtons
from telegrinder.types import InlineKeyboardMarkup

from src.bot.templates import render_template
from src.bot.utils.lessons import convert_schedule_to_pairs
from src.database import RepositoryFactory
from src.database.models import Group


@dataclasses.dataclass(slots=True, frozen=True)
class ScheduleCallbackData:
    date: str  # TODO: datetime.date now is not supported by telegrinder
    group_id: int
    subgroup: int
    is_week: bool = False


async def render_schedule_for_date(
    repository: RepositoryFactory,
    date: datetime.date,
    group: Group | None = None,
    sub_group: int = 1,
    is_week: bool = False,
) -> tuple[str, InlineKeyboardMarkup]:
    kb = InlineKeyboard()
    if not group:
        return "Вы не выбрали группу. Чтобы сделать это, введите /group", kb.get_markup()

    schedule = await repository.group.get_schedule(group.id, date)
    schedule = sorted(schedule, key=lambda x: x.time_slot.lesson_number)
    try:
        grouped_seminars, _ = convert_schedule_to_pairs(schedule, sub_group)
    except ValueError as e:
        return f"Ошибка при формировании расписания: {e}", kb.get_markup()
    is_schedule_subgrouped = len(set((item.subgroup for item in schedule))) > 1
    if is_schedule_subgrouped:
        kb.add(_get_subgroups_keyboard(group.id, date, sub_group, is_week=is_week))
    if is_week:
        kb.add(_get_week_keyboard(group.id, date, sub_group))

    if not schedule:
        return (
            f"Расписания {group.name} на {date.strftime('%d.%m.%Y')} не найдено",
            kb.get_markup(),
        )
    return render_template(
        "schedule.j2",
        {
            "grouped_seminars": grouped_seminars,
            "date": date,
            "group": group,
            "sub_group": sub_group if is_schedule_subgrouped else 0,
        },
    ), kb.get_markup()


def _get_week_keyboard(
    group_id: int, date: datetime.date, sub_group: int
) -> RowButtons[InlineButton]:
    buttons: list[InlineButton] = []

    week_days = _get_current_week(date)
    for day in week_days:
        buttons.append(
            InlineButton(
                day.strftime("%a" if day.day != date.day else "*%a*"),
                callback_data=ScheduleCallbackData(
                    date=day.strftime("%Y-%m-%d"),
                    group_id=group_id,
                    subgroup=sub_group,
                    is_week=True,
                ),
            )
        )
    return RowButtons(*buttons)


def _get_current_week(date: datetime.date) -> list[datetime.date]:
    monday = date - datetime.timedelta(days=date.weekday())
    week_days: list[datetime.date] = [monday + datetime.timedelta(days=i) for i in range(6)]
    return week_days


def _get_subgroups_keyboard(
    group_id: int,
    date: datetime.date,
    selected_subgroup: int,
    subgroups: Iterable[int] = (1, 2),
    is_week: bool = False,
) -> RowButtons[InlineButton]:
    buttons: list[InlineButton] = []
    for subgroup in subgroups:
        text = (
            f"*{subgroup} подгруппа*" if subgroup == selected_subgroup else f"{subgroup} подгруппа"
        )
        data = ScheduleCallbackData(
            subgroup=subgroup, date=date.strftime("%Y-%m-%d"), group_id=group_id, is_week=is_week
        )
        buttons.append(InlineButton(text, callback_data=data))
    return RowButtons(*buttons)
