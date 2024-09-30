from src.bot.client import bot
from src.bot.handlers import dispatches
from src.bot.utils.commands import update_commands

for dispatch in dispatches:
    bot.dispatch.load(dispatch)

bot.loop_wrapper.add_task(update_commands)
bot.run_forever()
