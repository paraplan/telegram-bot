from pydantic import BaseModel, Field

from paraplan.schedule.schemas.base import BaseItemSchema
from paraplan.schedule.schemas.group import GroupSchema
from paraplan.schedule.schemas.lecturer import LecturerSchema


class AreaSchema(BaseModel):
    info: BaseItemSchema = Field(validation_alias="area")
    color: str
    groups: list[GroupSchema]
    lecturers: list[LecturerSchema]
