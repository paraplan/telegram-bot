def main():
    from pathlib import Path

    from bot.client import bot
    from bot.utils.commands import update_commands

    bot.loop_wrapper.add_task(update_commands)
    bot.dispatch.load_from_dir(Path("packages", "bot", "src", "bot", "handlers"))
    bot.run_forever()
