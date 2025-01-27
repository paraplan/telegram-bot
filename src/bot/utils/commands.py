from telegrinder.types import BotCommand

from src.bot.client import api


async def update_commands():
    await api.set_my_commands(
        [
            BotCommand("start", "🤨"),
            BotCommand("group", "👥 Выбрать группу"),
            BotCommand("tomorrow", "📅 Расписание на завтра"),
            BotCommand("today", "📅 Расписание на сегодня"),
            BotCommand("monday", "📅 Расписание на понедельник"),
            BotCommand("week", "📅 Расписание на неделю"),
            BotCommand("settings", "⚙️ Настройки"),
        ]
    )
