from datetime import date
from enum import Enum
from typing import Literal

from loguru import logger
from telegrinder.types import ReplyKeyboardRemove

from src.bot.client import api
from src.database.repositories.factory import RepositoryFactory

NotificationType = Literal["schedule_updated", "schedule_added"]


class ScheduleType(Enum):
    DEFAULT = "is_notify"
    VACATION = "is_notify_vacation"
    PRACTICE = "is_notify_practice"
    SESSION = "is_notify_session"


async def send_notification(
    group_id: int,
    date: date,
    notification_type: NotificationType,
    schedule_type: ScheduleType,
):
    group = await RepositoryFactory().group.get(id=group_id)
    users = await RepositoryFactory().user.get_by_settings(
        group_id=group_id,
        is_notify=True,
        is_notify_vacation=schedule_type == ScheduleType.VACATION,
        is_notify_practice=schedule_type == ScheduleType.PRACTICE,
        is_notify_session=schedule_type == ScheduleType.SESSION,
    )
    text = {
        "schedule_updated": f"🔄 Обновлено расписание {group.name} на {date:<b>%A</b>, %d %B}",
        "schedule_added": f"🆕 Добавлено расписание {group.name} на {date:<b>%A</b>, %d %B}",
    }[notification_type]
    for user in users:
        logger.debug(f"send notification to user: {user}")
        await api.send_message(
            chat_id=user.id,
            text=text,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
        )
