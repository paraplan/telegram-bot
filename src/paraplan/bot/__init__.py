from pathlib import Path


def main() -> None:
    from paraplan.bot.client import bot
    from paraplan.bot.utils.commands import update_commands
    from paraplan.logging_configure import configure_logging

    configure_logging()
    bot.loop_wrapper.add_task(update_commands)
    bot.dispatch.load_from_dir(Path(__file__).with_name("handlers"))
    bot.run_forever()
