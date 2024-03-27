from datetime import time

from pydantic import BaseModel

from schedule_parser import BaseItem


class BellHour(BaseModel):
    start: time
    end: time


class Bells(BaseModel):
    id: BaseItem
    name: str
    hours: list[BellHour]
