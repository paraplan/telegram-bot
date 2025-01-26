from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database.client import engine
from src.database.repositories.day_type import DayTypeRepository
from src.database.repositories.group import GroupRepository
from src.database.repositories.lesson import LessonRepository
from src.database.repositories.room import RoomRepository
from src.database.repositories.schedule import ScheduleRepository
from src.database.repositories.subject import SubjectRepository
from src.database.repositories.time_slot import TimeSlotRepository
from src.database.repositories.user import UserRepository
from src.database.repositories.user_settings import UserSettingsRepository


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
