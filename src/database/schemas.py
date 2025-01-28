from enum import Enum


class ScheduleType(Enum):
    DEFAULT = "is_notify"
    VACATION = "is_notify_vacation"
    PRACTICE = "is_notify_practice"
    SESSION = "is_notify_session"
