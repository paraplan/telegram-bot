from typing import Self

from pydantic import BaseModel

from src.bot.templates import datetime_filter
from src.database.generated import GetScheduleByGroupResultSeminarsItem


class GroupedSeminar(BaseModel):
    name: str
    time: str
    cabinet: str | None = None

    def __add__(self, obj: Self) -> Self:
        _separator = " | "
        self.name = f"{self.name}{_separator}{obj.name}"
        self.time = f"{self.time}, {obj.time}"
        self.cabinet = f"{self.cabinet} | {obj.cabinet}"
        return self


def group_seminars_for_numbers(seminars: list[GetScheduleByGroupResultSeminarsItem]):
    result: dict[int, GroupedSeminar] = dict()
    subgrouped_seminars: dict[int, GroupedSeminar] = dict()
    i = 0
    first_seminar_index: int = -1
    while i < len(seminars) - 1:
        current_seminar, next_seminar = (
            seminars[i],
            seminars[i + 1],
        )
        name = current_seminar.subject.name
        cabinet = None
        if current_seminar.cabinet:
            cabinet = current_seminar.cabinet.room
        time = (
            f"{datetime_filter(current_seminar.start_time)}"
            f" - {datetime_filter(current_seminar.end_time)}"
        )
        if current_seminar.number == next_seminar.number:
            name = f"{current_seminar.subject.name} | {next_seminar.subject.name}"
            if current_seminar.subject.name == next_seminar.subject.name:
                name = current_seminar.subject.name
        if first_seminar_index == -1 or current_seminar.number < first_seminar_index:
            first_seminar_index = current_seminar.number
        subgrouped_seminars.update(
            {current_seminar.number: GroupedSeminar(name=name, time=time, cabinet=cabinet)}
        )
        i += 1
    subgrouped_indexes = subgrouped_seminars.keys()
    last_cheked: str = ""
    for i in subgrouped_indexes:
        if subgrouped_seminars.get(i + 1):
            if subgrouped_seminars[i].name == subgrouped_seminars[i + 1].name:
                if last_cheked == subgrouped_seminars[i]:
                    last_cheked = ""
                    continue
                last_cheked = subgrouped_seminars[i].name
                subgrouped_seminars[
                    i
                ].time = f"{subgrouped_seminars[i].time}, {subgrouped_seminars[i + 1].time}"
                result.update({i // 2 + 1: subgrouped_seminars[i]})
            else:
                result.update({i // 2 + 1: subgrouped_seminars[i] + subgrouped_seminars[i + 1]})
    return result
