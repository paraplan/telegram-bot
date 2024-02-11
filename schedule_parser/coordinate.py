from copy import deepcopy
from dataclasses import dataclass

from schedule_parser.client import work_sheet


@dataclass(slots=True)
class Coordinate:
    row: int
    column: int

    def _get_cell(self):
        return work_sheet.cell(self.row, self.column)

    def _get_merged_cells_range(self):
        return [s for s in work_sheet.merged_cells.ranges if self._get_cell().coordinate in s]

    def get_cell_value(self) -> str:
        """Get merged cell value"""
        range = self._get_merged_cells_range()
        result = (
            work_sheet.cell(range[0].min_row, range[0].min_col).value
            if len(range) != 0
            else self._get_cell().value
        )
        return str(result) if result else ""

    def get_merged_cells(self) -> list["Coordinate"]:
        """Get merged cells"""
        range = self._get_merged_cells_range()
        return (
            [Coordinate(cell[0], cell[1]) for cell in range[0].bottom] if len(range) != 0 else []
        )

    def copy(self, row_offset: int = 0, column_offset: int = 0) -> "Coordinate":
        copy = deepcopy(self)
        copy.row += row_offset
        copy.column += column_offset
        return copy
