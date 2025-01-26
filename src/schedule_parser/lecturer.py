from pydantic import BaseModel, Field, field_validator

from src.schedule_parser.base import BaseItemSchema

LecturerHourType = list["LecturerHourSchema"]


class LecturerHourSchema(BaseModel):
    group_name: str = Field(validation_alias="group")
    room: BaseItemSchema | None


class LecturerSchema(BaseModel):
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

    info: BaseItemSchema = Field(validation_alias="lecturer")
    hours: dict[int, list[LecturerHourSchema]]
