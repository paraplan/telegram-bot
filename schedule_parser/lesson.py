from dataclasses import dataclass

from schedule_parser.cabinets import parse_cabinets
from schedule_parser.coordinate import Coordinate


@dataclass(slots=True, frozen=True)
class Lesson:
    title: str
    cabinets: list[str]
    group_name: str


def parse_lesson(lesson_coordinate: Coordinate, header_distance: int) -> Lesson:
    title: str = lesson_coordinate.get_cell_value()
    cabinets = parse_cabinets(
        lesson_coordinate.copy(column_offset=len(lesson_coordinate.get_merged_cells()) or 1),
        header_distance,
    )
    group_name: str = lesson_coordinate.copy(row_offset=-header_distance - 1).get_cell_value()
    return Lesson(title=title, cabinets=cabinets, group_name=group_name)
