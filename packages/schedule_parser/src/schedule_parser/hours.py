from pydantic import BaseModel

from schedule_parser.base import BaseItemSchema


class HourSchema(BaseModel):
    occupation: str
    room: BaseItemSchema | None = None
