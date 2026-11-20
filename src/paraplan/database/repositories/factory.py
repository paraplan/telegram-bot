from sqlalchemy.ext.asyncio import async_sessionmaker

from paraplan.database.client import engine
from paraplan.database.repositories.day_type import DayTypeRepository
from paraplan.database.repositories.group import GroupRepository
from paraplan.database.repositories.lesson import LessonRepository
from paraplan.database.repositories.room import RoomRepository
from paraplan.database.repositories.schedule import ScheduleRepository
from paraplan.database.repositories.subject import SubjectRepository
from paraplan.database.repositories.time_slot import TimeSlotRepository
from paraplan.database.repositories.user import UserRepository
from paraplan.database.repositories.user_settings import UserSettingsRepository


class RepositoryFactory:
    def __init__(self):
        self._sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

        self.room = RoomRepository(self._sessionmaker)
        self.group = GroupRepository(self._sessionmaker)
        self.subject = SubjectRepository(self._sessionmaker)
        self.lesson = LessonRepository(self._sessionmaker)
        self.day_type = DayTypeRepository(self._sessionmaker)
        self.time_slot = TimeSlotRepository(self._sessionmaker)
        self.schedule = ScheduleRepository(self._sessionmaker)
        self.user = UserRepository(self._sessionmaker)
        self.user_settings = UserSettingsRepository(self._sessionmaker)
