import datetime
import functools
import re
from collections.abc import Awaitable
from typing import Any, Callable, TypeVar

from src.bot.utils.notification import send_notification
from src.database import RepositoryFactory
from src.database.models import Lesson
from src.database.schemas import ScheduleType
from src.schedule_parser.area import AreaSchema
from src.schedule_parser.group import GroupSchema

T = TypeVar("T")


def check_lesson_updates(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    """
    Decorator that checks if lessons were updated after function execution.
    """

    @functools.wraps(func)
    async def wrapper(
        repository: RepositoryFactory,
        area: AreaSchema,
        group: GroupSchema,
        schedule_date: datetime.date,
        *args: Any,
        **kwargs: Any,
    ) -> T:
        old_lessons = await repository.lesson.get(group_id=group.info.id, date=schedule_date)
        old_lesson_ids = sorted(map(lambda x: x.id, old_lessons))

        result = await func(repository, area, group, schedule_date, *args, **kwargs)

        new_lessons = await repository.lesson.get(group_id=group.info.id, date=schedule_date)
        new_lesson_ids = sorted(map(lambda x: x.id, new_lessons))

        if old_lesson_ids == []:
            await send_notification(
                group.info.id, schedule_date, "schedule_added", check_lesson_types(new_lessons)
            )
        elif old_lesson_ids != new_lesson_ids:
            await send_notification(
                group.info.id, schedule_date, "schedule_updated", check_lesson_types(new_lessons)
            )
        return result

    return wrapper


def check_lesson_types(lessons: list[Lesson]) -> ScheduleType:
    lesson_types = set(map(lambda x: x.subject.name.lower(), lessons))
    if all(re.match(r"^практика\s*\w*$", lesson_type) for lesson_type in lesson_types):
        return ScheduleType.PRACTICE
    elif lesson_types == {"сессия"}:
        return ScheduleType.SESSION
    elif lesson_types == {"каникулы"}:
        return ScheduleType.VACATION
    return ScheduleType.DEFAULT
