from datetime import time

from pydantic import BaseModel

from src.schedule_parser.base import BaseItem


class BellsHours(BaseModel):
    start: time
    end: time


class Bells(BaseModel):
    name: str
    id: BaseItem
    hours: list[BellsHours]
