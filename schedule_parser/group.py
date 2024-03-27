from pydantic import BaseModel, Field, RootModel

from schedule_parser import BaseItem
from schedule_parser.schedule import Lesson


class SubGroupSchedules(RootModel):
    root: dict[int, Lesson]


class GroupInfo(BaseModel):
    schedules: dict[int, SubGroupSchedules] = Field(validation_alias="schedule")
    group: BaseItem
