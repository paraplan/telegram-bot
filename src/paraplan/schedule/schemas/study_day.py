from datetime import date

from pydantic import BaseModel

from paraplan.schedule.schemas.area import AreaSchema
from paraplan.schedule.schemas.bells import BellsSchema


class StudyDaySchema(BaseModel):
    date: date
    bells: BellsSchema
    areas: list[AreaSchema]
