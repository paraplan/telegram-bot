from pydantic import BaseModel, Field, field_validator

from schedule_parser.base import BaseItemSchema
from schedule_parser.hours import HourSchema

LessonType = dict[int, HourSchema]
HoursType = dict[int, LessonType]


class GroupSchema(BaseModel):
    @field_validator("hours", mode="before")
    def validate_hours(cls, hours: HoursType | list[LessonType]) -> HoursType:
        """
        Converts the list to the dict.
        Because hours is a list when the pairs start at zero
        and a dict when the pairs start at one (🤡).
        """
        if isinstance(hours, list):
            return {index: hour for index, hour in enumerate(hours)}
        return hours

    info: BaseItemSchema = Field(validation_alias="group")
    extramural: bool
    course: int
    number: int
    prefix: str
    hours: HoursType
