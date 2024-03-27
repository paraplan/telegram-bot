from pydantic import BaseModel

from schedule_parser import BaseItem


class Lesson(BaseModel):
    lecturer: BaseItem | None
    room: BaseItem | None
    type: int
    occupation: BaseItem
