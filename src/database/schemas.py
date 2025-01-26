import datetime

from pydantic import BaseModel


class GroupCreate(BaseModel):
    id: int
    name: str
    full_name: str


class CabinetCreate(BaseModel):
    id: int
    location: str
    description: str


class LecturerCreate(BaseModel):
    id: int
    name: str
    full_name: str


class SeminarCreate(BaseModel):
    number: int
    occupation: str
    date: datetime.date
    bell_id: int
    cabinet_id: int | None = None
    lecturer_id: int | None = None


class BellCreate(BaseModel):
    start_time: datetime.time
    end_time: datetime.time
