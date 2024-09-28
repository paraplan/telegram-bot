import logging
from datetime import date

from src.bot.client import api, db_client
from src.database.generated import GetAllGroupsResult, get_group_students

logger = logging.getLogger(__name__)


async def send_notification(group: GetAllGroupsResult, date: date, old_seminars, new_seminars):
    group_students = await get_group_students(db_client, group_id=group.id)
    for student in group_students:
        logger.debug("send notification to student: %s", student)
        await api.send_message(
            chat_id=student.telegram_id,
            text=f"Обновлено расписание на {date} для группы {group.name}",
        )
