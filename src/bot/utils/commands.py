from telegrinder.types import BotCommand

from src.bot.client import api


async def update_commands():
    await api.set_my_commands(
        commands=[
            BotCommand("start", "🤨"),
            BotCommand("group", "👥 Выбрать группу"),
            BotCommand("next", "📆 Расписание на ближайший день"),
            BotCommand("today", "📅 Расписание на сегодня"),
            BotCommand("monday", "📅 Расписание на понедельник"),
            BotCommand("week", "📅 Расписание на неделю"),
            BotCommand("date", "📅 Расписание на дату"),
            BotCommand("subgroup", "➗Выбрать подгруппу"),
            BotCommand("settings", "⚙️ Настройки"),
            BotCommand("version", "📘 Версия бота"),
        ]
    )
