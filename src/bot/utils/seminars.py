from typing import Self

from pydantic import BaseModel

from src.bot.templates import datetime_filter
from src.database.generated import GetScheduleByGroupResultSeminarsItem


class GroupedSeminar(BaseModel):
    name: str
    time: str
    cabinet: str | None = None
    is_half: bool = True

    def __add__(self, obj: Self) -> Self:
        self.name = f"{self.name} | {obj.name}" if self.name != obj.name else self.name
        self.time = (
            f"{self.time}, {obj.time}" if self.time.split(", ")[-1] != obj.time else self.time
        )
        self.cabinet = f"{self.cabinet} | {obj.cabinet}"
        return self


def group_seminars_for_numbers(seminars: list[GetScheduleByGroupResultSeminarsItem]):
    result: dict[int, GroupedSeminar] = dict()
    subgroup_seminars: dict[int, GroupedSeminar] = dict()
    i = 0
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
        subgroup_seminars.update(
            {current_seminar.number: GroupedSeminar(name=name, time=time, cabinet=cabinet)}
        )
        i += 1

    subgroup_indexes = subgroup_seminars.keys()
    last_checked: str = ""
    for i in subgroup_indexes:
        if subgroup_seminars.get(i + 1):
            if subgroup_seminars[i].name == subgroup_seminars[i + 1].name:
                if last_checked == subgroup_seminars[i]:
                    last_checked = ""
                    continue
                last_checked = subgroup_seminars[i].name
                subgroup_seminars[
                    i
                ].time = f"{subgroup_seminars[i].time}, {subgroup_seminars[i + 1].time}"
                result.update({i // 2 + 1: subgroup_seminars[i]})
            else:
                result.update({i // 2 + 1: subgroup_seminars[i] + subgroup_seminars[i + 1]})
        else:
            if result[i // 2].name == subgroup_seminars[i].name:
                result.update({i // 2: result[i // 2] + subgroup_seminars[i]})
            else:
                result.update({i // 2 + 1: subgroup_seminars[i]})
    return result
