from pydantic import BaseModel

from paraplan.schedule.schemas.base import BaseItemSchema


class HourSchema(BaseModel):
    occupation: str
    room: BaseItemSchema | None = None
    subgroups: int | None = None
