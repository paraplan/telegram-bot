import logging
from datetime import date
from typing import Literal

from telegrinder.types import ReplyKeyboardRemove

from src.bot.client import api
from src.database.models import Group

logger = logging.getLogger(__name__)


NotificationType = Literal["schedule_updated", "schedule_added"]


async def send_notification(group: Group, date: date, notification_type: NotificationType):
    text = {
        "schedule_updated": f"🔄 Обновлено расписание {group.name} на {date:<b>%A</b>, %d %B}",
        "schedule_added": f"🆕 Добавлено расписание {group.name} на {date:<b>%A</b>, %d %B}",
    }[notification_type]
    logger.debug(group.users)
    for user in group.users:
        logger.debug("send notification to user: %s", user)
        await api.send_message(
            chat_id=user.id,
            text=text,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
        )
