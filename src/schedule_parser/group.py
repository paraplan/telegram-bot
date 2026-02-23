from typing import Annotated, TypeAlias, TypeVar

from pydantic import BaseModel, BeforeValidator, Field

from src.schedule_parser.base import BaseItemSchema
from src.schedule_parser.hours import HourSchema

T = TypeVar("T")
WetAssociativeType: TypeAlias = dict[int, T]
DryAssociativeType: TypeAlias = WetAssociativeType[T] | list[T]


def normalize_associative(v: DryAssociativeType[T]) -> WetAssociativeType[T]:
    if isinstance(v, list):
        return {i: item for i, item in enumerate(v)}
    return v


HoursType: TypeAlias = Annotated[
    WetAssociativeType[HourSchema], BeforeValidator(normalize_associative)
]


class GroupSchema(BaseModel):
    info: BaseItemSchema = Field(validation_alias="group")
    extramural: bool
    course: int
    number: int
    prefix: str
    hours: Annotated[WetAssociativeType[HoursType], BeforeValidator(normalize_associative)]
