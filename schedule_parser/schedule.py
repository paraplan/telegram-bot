from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from schedule_parser.client import work_sheet
from schedule_parser.coordinate import Coordinate
from schedule_parser.env import START_COLUMN, START_ROW
from schedule_parser.section import Section, parse_section


@dataclass(slots=True, frozen=True)
class Schedule:
    sections: list[Section]
    date: date


def parse_schedule(schedule_data: Any) -> Schedule:
    sections: list[Section] = []
    base_coordinate = Coordinate(START_ROW, START_COLUMN)
    while base_coordinate.get_cell_value().strip() != "":
        section = parse_section(base_coordinate)
        sections.append(section)
        base_coordinate.row = section.end_row + 3
    now: datetime = datetime.now()
    return Schedule(sections, date(now.year, *map(int, work_sheet.title.split("."))))
