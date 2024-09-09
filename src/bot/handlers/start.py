from telegrinder import Dispatch, Message
from telegrinder.rules import Command

dp = Dispatch()


@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer(
        "Для того чтобы получить расписание на завтра отправьте команду /next_day"
    )
