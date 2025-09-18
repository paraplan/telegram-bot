from telegrinder.types import BotCommand

from src.bot.client import api


async def update_commands():
    await api.set_my_commands(
        commands=[
            BotCommand("start", "🤨"),
            BotCommand("group", "👥 Выбрать группу"),
            BotCommand("next", "📆 Ближайшее расписание"),
            BotCommand("week", "📅 Расписание текущей недели"),
            BotCommand("date", "🗓 Расписание по дате"),
            BotCommand("subgroup", "➗Выбрать подгруппу"),
            BotCommand("settings", "⚙️ Настройки"),
            BotCommand("version", "📘 Версия бота"),
        ]
    )
