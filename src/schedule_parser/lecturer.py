from pydantic import BaseModel, Field, field_validator

from src.schedule_parser.base import BaseItem

LecturerHourType = list["LecturerHour"]


class LecturerHour(BaseModel):
    group_name: str = Field(validation_alias="group")
    room: BaseItem | None


class Lecturer(BaseModel):
    @field_validator("hours", mode="before")
    def validate_hours(
        cls, hours: dict[int, LecturerHourType] | list[LecturerHourType]
    ) -> dict[int, LecturerHourType]:
        """
        Converts the list to the dict.
        Because hours is a list when the pairs start at zero
        and a dict when the pairs start at one (🤡).
        """
        if isinstance(hours, list):
            return {index: hour for index, hour in enumerate(hours)}
        return hours

    info: BaseItem = Field(validation_alias="lecturer")
    hours: dict[int, list[LecturerHour]]
