from typing import Self

from pydantic import BaseModel

from src.bot.utils.datetime import datetimes_filter
from src.database.generated import GetScheduleByGroupResultSeminarsItem


class GroupedSeminar(BaseModel):
    name: str
    number: int
    time: str
    cabinet: str | None = None

    def __add__(self, next: Self) -> Self:
        if self.number == next.number:
            if self.name == next.name:
                self.cabinet = f"{self.cabinet} | {next.cabinet}"
                return self
        return self


SeminarsType = dict[int, list[GroupedSeminar]]


def convert_schedule_to_seminars(
    schedule: list[GetScheduleByGroupResultSeminarsItem],
) -> SeminarsType:
    seminars: SeminarsType = dict()
    for seminar in schedule:
        item = GroupedSeminar(
            name=seminar.subject.name,
            number=seminar.number,
            time=datetimes_filter((seminar.start_time, seminar.end_time)),
            cabinet=seminar.cabinet.room if seminar.cabinet else None,
        )
        if not seminars.get(seminar.number):
            seminars[seminar.number] = []
        seminars[seminar.number].append(item)
    return seminars


def _group_seminar(items: list[GroupedSeminar]) -> GroupedSeminar:
    result = items[0]
    for item in items:
        if item == result:
            continue
        result = result + item
    return result


def group_seminars(seminars: SeminarsType) -> dict[int, GroupedSeminar]:
    grouped_seminars: dict[int, GroupedSeminar] = dict()
    for index, item in seminars.items():
        grouped_seminars[index] = _group_seminar(item)
    return grouped_seminars


class PairModel(BaseModel):
    name: str
    time: str
    cabinet: str | None = None


def _process_cabinets(cabinets: tuple[str | None, str | None]) -> str:
    if (
        cabinets[0]
        and cabinets[1]
        and set(cabinets[0].split(" | ")) == set(cabinets[1].split(" | "))
    ):
        return cabinets[0]
    if cabinets[0] == cabinets[1]:
        return cabinets[0] or "??"
    result = [cabinets[0] or "??", cabinets[1] or "??"]
    return " | ".join(result)


def convert_seminars_to_pairs(seminars: dict[int, GroupedSeminar]):
    pairs: dict[int, PairModel] = dict()
    seminars_keys = list(seminars.keys())
    i: int = seminars_keys[0]
    while i <= seminars_keys[-2]:
        seminar, next_seminar = seminars[i], seminars[i + 1]

        if seminar.name == next_seminar.name:
            name = seminar.name
        else:
            name = f"{seminar.name} | {next_seminar.name}"
        cabinet = _process_cabinets((seminar.cabinet, next_seminar.cabinet))
        time = f"{seminar.time}, {next_seminar.time}"
        pair = PairModel(name=name, cabinet=cabinet, time=time)
        pairs[seminar.number // 2 + 1] = pair

        if i == seminars_keys[-2]:
            break
        i += 2
    return pairs


def convert_schedule_to_pairs(schedule: list[GetScheduleByGroupResultSeminarsItem]) -> dict:
    seminars = convert_schedule_to_seminars(schedule)
    grouped_seminars = group_seminars(seminars)
    pairs = convert_seminars_to_pairs(grouped_seminars)
    return pairs
