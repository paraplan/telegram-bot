from pydantic import BaseModel

from src.schedule_parser.base import BaseItem


class Hour(BaseModel):
    occupation: str
    room: BaseItem | None = None
