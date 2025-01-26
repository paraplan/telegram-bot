import datetime
import functools
from collections.abc import Awaitable
from typing import Any, Callable, TypeVar

from src.bot.utils.notification import send_notification
from src.database import RepositoryFactory
from src.schedule_parser.group import GroupSchema

T = TypeVar("T")


def check_lesson_updates(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    """
    Decorator that checks if lessons were updated after function execution.
    """

    @functools.wraps(func)
    async def wrapper(
        repository: RepositoryFactory,
        group: GroupSchema,
        schedule_date: datetime.date,
        *args: Any,
        **kwargs: Any,
    ) -> T:
        old_lessons = await repository.lesson.get(group_id=group.info.id, date=schedule_date)
        old_lesson_ids = sorted(map(lambda x: x.id, old_lessons))

        result = await func(repository, group, schedule_date, *args, **kwargs)

        new_lessons = await repository.lesson.get(group_id=group.info.id, date=schedule_date)
        new_lesson_ids = sorted(map(lambda x: x.id, new_lessons))

        if old_lesson_ids != new_lesson_ids:
            group_db = await repository.group.get(id=group.info.id)
            await send_notification(group_db, schedule_date, "schedule_added")
        elif old_lessons and new_lessons:
            group_db = await repository.group.get(id=group.info.id)
            # Sort lessons by ID for consistent comparison
            old_sorted = sorted(old_lessons, key=lambda x: x.id)
            new_sorted = sorted(new_lessons, key=lambda x: x.id)

            for old, new in zip(old_sorted, new_sorted, strict=True):
                if (
                    old.subject_id != new.subject_id
                    or old.teacher_id != new.teacher_id
                    or old.room_id != new.room_id
                    or old.time_slot_id != new.time_slot_id
                ):
                    await send_notification(group_db, schedule_date, "schedule_updated")
        return result

    return wrapper
