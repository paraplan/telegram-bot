from .cabinet import CabinetRepository
from .couple import CoupleRepository
from .lecturer import LecturerRepository
from .lesson import LessonRepository


class DatabaseRepository:
    cabinet = CabinetRepository()
    lecturer = LecturerRepository()
    lesson = LessonRepository()
    couple = CoupleRepository()
