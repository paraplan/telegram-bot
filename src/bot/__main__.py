from src.bot.client import bot, update_commands
from src.bot.handlers import dispatches

for dispatch in dispatches:
    bot.dispatch.load(dispatch)


bot.loop_wrapper.add_task(update_commands)
bot.run_forever()
