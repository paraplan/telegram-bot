from typing import Self

from pydantic import BaseModel

from src.bot.utils.datetime import datetimes_filter
from src.database.models import Lesson


class GroupedSeminar(BaseModel):
    name: str
    number: int
    time: str
    sub_group: int
    cabinet: str | None

    def merge(self, second: Self, sub_group: int = 0) -> Self:
        if sub_group != 0:
            if self.sub_group != sub_group and second.sub_group == sub_group:
                return second
        else:
            if self.name == second.name:
                self.cabinet = _process_cabinets((self.cabinet, second.cabinet), separator=", ")
        return self


SeminarsType = dict[int, list[GroupedSeminar]]


def convert_schedule_to_seminars(schedule: list[Lesson]) -> SeminarsType:
    seminars: SeminarsType = dict()
    for schedule_seminar in schedule:
        seminar = schedule_seminar
        item = GroupedSeminar(
            name=seminar.subject.name,
            number=seminar.time_slot.lesson_number,
            time=datetimes_filter((seminar.time_slot.start_time, seminar.time_slot.end_time)),
            sub_group=schedule_seminar.subgroup,
            cabinet=seminar.room.room_number if seminar.room else None,
        )
        if not seminars.get(seminar.time_slot.lesson_number):
            seminars[seminar.time_slot.lesson_number] = []
        seminars[seminar.time_slot.lesson_number].append(item)
    return seminars


def _group_seminar(items: list[GroupedSeminar], sub_group: int = 0) -> tuple[GroupedSeminar, bool]:
    result = items[0]
    is_schedule_subgrouped = False
    items_subgroups = set((item.sub_group for item in items if item.name != "Физкультура"))
    if len(items_subgroups) > 1:
        is_schedule_subgrouped = True
    if len(items_subgroups) > 2:
        sub_group = 0
        is_schedule_subgrouped = True
    for item in items:
        if item == result:
            continue
        result = result.merge(item, sub_group)
    return result, is_schedule_subgrouped


def group_seminars(
    seminars: SeminarsType, sub_group: int = 0
) -> tuple[dict[int, GroupedSeminar], bool]:
    grouped_seminars: dict[int, GroupedSeminar] = dict()
    is_schedule_subgrouped = False
    for index, item in seminars.items():
        result = _group_seminar(item, sub_group)
        if result[1]:
            is_schedule_subgrouped = True
        grouped_seminars[index] = result[0]
    return grouped_seminars, is_schedule_subgrouped


class PairModel(BaseModel):
    name: str
    time: str
    cabinet: str | None


def _process_cabinets(
    cabinets: tuple[str | None, str | None], separator: str = " | "
) -> str | None:
    if (
        cabinets[0]
        and cabinets[1]
        and set(cabinets[0].split(separator)) == set(cabinets[1].split(separator))
    ):
        return cabinets[0]
    if cabinets[0] == cabinets[1]:
        return cabinets[0]
    result = [cabinets[0] or "None", cabinets[1]]
    return separator.join(result)


def convert_seminars_to_pairs(seminars: dict[int, GroupedSeminar], sub_group: int = 1):
    pairs: dict[int, PairModel] = dict()
    seminars_keys = list(seminars.keys())
    is_schedule_subgrouped = False if sub_group != 0 else True
    i: int = seminars_keys[0]
    while i <= seminars_keys[-2]:
        seminar, next_seminar = seminars[i], seminars[i + 1]
        if (
            sub_group == 1
            and seminar.sub_group != sub_group
            and next_seminar.sub_group != sub_group
        ):
            i += 2
            is_schedule_subgrouped = True
            continue
        if seminar.number % 2 == 0:
            pair = PairModel(
                name="None | " + seminar.name, cabinet=seminar.cabinet, time=seminar.time
            )
            pairs[seminar.number // 2] = pair
            i += 1
            continue

        if seminar.name == next_seminar.name:
            name = seminar.name
        else:
            name = f"{seminar.name} | {next_seminar.name}"
        cabinet = _process_cabinets((seminar.cabinet, next_seminar.cabinet))
        seminar_times = seminar.time.split(" - ")
        next_seminar_time = next_seminar.time.split(" - ")
        if seminar_times[1] == next_seminar_time[0]:
            time = f"{seminar_times[0]} - {next_seminar_time[1]}"
        else:
            time = f"{seminar.time}, {next_seminar.time}"
        pair = PairModel(name=name, cabinet=cabinet, time=time)
        pairs[seminar.number // 2 + 1] = pair

        i += 2
    if seminars.get(i):
        pairs[i // 2 + 1] = PairModel(
            name=seminars[i].name, time=seminars[i].time, cabinet=seminars[i].cabinet
        )
    return pairs, is_schedule_subgrouped


def convert_schedule_to_pairs(schedule: list[Lesson], sub_group: int = 0) -> tuple[dict, bool]:
    if not schedule:
        return {}, False
    seminars = convert_schedule_to_seminars(schedule)
    grouped_seminars = group_seminars(seminars, sub_group)
    pairs = convert_seminars_to_pairs(grouped_seminars[0], sub_group)
    return pairs[0], grouped_seminars[1] or pairs[1]
