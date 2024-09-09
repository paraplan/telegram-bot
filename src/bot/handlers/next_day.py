from telegrinder import Dispatch, Message
from telegrinder.rules import Command

from src.bot.client import MiddlewareUser

dp = Dispatch()


@dp.message(Command("next_day"))
async def handle_next_day(message: Message, user: MiddlewareUser):
    if user.group is None:
        await message.answer("Вы не выбрали группу. Чтобы сделать это, введите /group")
        return
    await message.answer("Расписание на завтра")
