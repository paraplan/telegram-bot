from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

from src.schedule_parser.base import BaseItemSchema
from src.schedule_parser.hours import HourSchema

type WetAssociativeType[T] = dict[int, T]
type DryAssociativeType[T] = WetAssociativeType[T] | list[T]


def normalize_associative[T](v: DryAssociativeType[T]) -> WetAssociativeType[T]:
    if isinstance(v, list):
        return {i: item for i, item in enumerate(v)}
    return v


type HoursType = Annotated[WetAssociativeType[HourSchema], BeforeValidator(normalize_associative)]


class GroupSchema(BaseModel):
    info: BaseItemSchema = Field(validation_alias="group")
    extramural: bool
    course: int
    number: int
    prefix: str
    hours: Annotated[WetAssociativeType[HoursType], BeforeValidator(normalize_associative)]
