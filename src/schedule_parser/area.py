from pydantic import BaseModel, Field

from src.schedule_parser.base import BaseItemSchema
from src.schedule_parser.group import GroupSchema
from src.schedule_parser.lecturer import LecturerSchema


class AreaSchema(BaseModel):
    info: BaseItemSchema = Field(validation_alias="area")
    color: str
    groups: list[GroupSchema]
    lecturers: list[LecturerSchema]
