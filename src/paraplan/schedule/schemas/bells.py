from datetime import time

from pydantic import BaseModel, Field

from paraplan.schedule.schemas.base import BaseItemSchema


class BellsHoursSchema(BaseModel):
    start: time
    end: time


class BellsSchema(BaseModel):
    name: str
    info: BaseItemSchema = Field(validation_alias="id")
    hours: list[BellsHoursSchema]
