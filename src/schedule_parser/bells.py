from datetime import time

from pydantic import BaseModel, Field

from src.schedule_parser.base import BaseItemSchema


class BellsHoursSchema(BaseModel):
    start: time
    end: time


class BellsSchema(BaseModel):
    name: str
    info: BaseItemSchema = Field(validation_alias="id")
    hours: list[BellsHoursSchema]
