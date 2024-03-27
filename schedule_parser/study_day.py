from datetime import date

from pydantic import BaseModel

from schedule_parser import BaseItem
from schedule_parser.group import GroupInfo


class StudyDay(BaseModel):
    date: date
    groups: dict[int, GroupInfo]
    bells: BaseItem
