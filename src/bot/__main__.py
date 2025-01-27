from pathlib import Path

from src.bot.client import bot
from src.bot.utils.commands import update_commands

bot.loop_wrapper.add_task(update_commands)
bot.dispatch.load_from_dir(Path("src", "bot", "handlers"))
bot.run_forever()
