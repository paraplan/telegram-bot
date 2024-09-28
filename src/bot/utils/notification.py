from datetime import date

from src.bot.client import api
from src.database.generated import GetAllGroupsResult


async def send_notification(group: GetAllGroupsResult, date: date, old_seminars, new_seminars):
    await api.send_message(
        chat_id=735365900,  # TODO: change hardcode id to ids for group members
        text=f"Обновлено расписание на {date} для группы {group.name}\n\n"
        f"Старые семинары: {old_seminars}\nНовые семинары: {new_seminars}",
    )
