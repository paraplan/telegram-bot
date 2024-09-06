from datetime import date

from pydantic import BaseModel

from src.schedule_parser.area import Area
from src.schedule_parser.bells import Bells


class StudyDay(BaseModel):
    date: date
    bells: Bells
    areas: list[Area]
