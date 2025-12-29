from datetime import date

from pydantic import BaseModel

from schedule_parser.area import AreaSchema
from schedule_parser.bells import BellsSchema


class StudyDaySchema(BaseModel):
    date: date
    bells: BellsSchema
    areas: list[AreaSchema]
