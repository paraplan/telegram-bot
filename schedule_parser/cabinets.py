from schedule_parser.coordinate import Coordinate


def parse_cabinets_count(cabinets_coordinate: Coordinate, header_distance: int) -> int:
    return len(cabinets_coordinate.copy(row_offset=-header_distance - 1).get_merged_cells()) or 1


def parse_cabinets(cabinets_coordinate: Coordinate, header_distance: int) -> list[str]:
    cabinets: list[str] = []
    for i in range(parse_cabinets_count(cabinets_coordinate, header_distance)):
        cabinet = cabinets_coordinate.copy(column_offset=i).get_cell_value()
        if cabinet not in cabinets and cabinet.strip() != "":
            cabinets.append(cabinet)
    return cabinets
