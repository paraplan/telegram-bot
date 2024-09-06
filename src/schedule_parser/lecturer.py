from pydantic import BaseModel, Field

from src.schedule_parser.base import BaseItem


class LecturerHour(BaseModel):
    group_name: str = Field(validation_alias="group")
    room: BaseItem | None


class Lecturer(BaseModel):
    info: BaseItem = Field(validation_alias="lecturer")
    hours: dict[int, list[LecturerHour]]
