from datetime import date
from typing import Literal

from loguru import logger
from telegrinder.types import ReplyKeyboardRemove

from src.bot.client import api
from src.database.repositories.factory import RepositoryFactory
from src.database.schemas import ScheduleType

NotificationType = Literal["schedule_updated", "schedule_added"]


async def send_notification(
    group_id: int,
    date: date,
    notification_type: NotificationType,
    schedule_type: ScheduleType,
):
    group = await RepositoryFactory().group.get(id=group_id)
    users = await RepositoryFactory().user.get_by_settings(
        group_id=group_id, schedule_type=schedule_type
    )
    emoji = {
        ScheduleType.DEFAULT: "🆕",
        ScheduleType.VACATION: "🏖️",
        ScheduleType.PRACTICE: "💻",
        ScheduleType.SESSION: "📚",
    }[schedule_type]
    text = {
        "schedule_updated": f"🔄 Обновлено расписание {group.name} на {date:<b>%A</b>, %d %B}",
        "schedule_added": f"{emoji} Добавлено расписание {group.name} на {date:<b>%A</b>, %d %B}",
    }[notification_type]
    for user in users:
        logger.debug(f"send notification to user: {user}")
        await api.send_message(
            chat_id=user.id,
            text=text,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
        )
