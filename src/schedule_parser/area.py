from pydantic import BaseModel, Field

from src.schedule_parser.base import BaseItem
from src.schedule_parser.group import Group
from src.schedule_parser.lecturer import Lecturer


class Area(BaseModel):
    info: BaseItem = Field(validation_alias="area")
    color: str
    groups: list[Group]
    lecturers: list[Lecturer]
