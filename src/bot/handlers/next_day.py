import datetime
from collections import defaultdict

from telegrinder import Dispatch, Message
from telegrinder.rules import Command

from src.bot.client import MiddlewareUser, db_client, formatter
from src.bot.templates import render_template
from src.database.generated import get_schedule_by_group

dp = Dispatch()


@dp.message(Command("next_day"))
async def handle_next_day(message: Message, user: MiddlewareUser):
    if user.group is None:
        await message.answer("Вы не выбрали группу. Чтобы сделать это, введите /group")
        return
    date = message.date + datetime.timedelta(days=1)
    schedule = (
        await get_schedule_by_group(
            db_client,
            group_id=user.group.id,
            date=date,
        ),
    )[0]
    if not schedule:
        await message.answer("Нет расписания на этот день")
        return
    #  TODO: very bad code
    subgroups_seminars = defaultdict(list)
    for seminar in schedule.seminars:
        subgroups_seminars[seminar.number].append(seminar)
    pairs_seminars = dict()
    for number, seminars in subgroups_seminars.items():
        key = (number - 1) // 2 + 1
        if number not in pairs_seminars:
            pairs_seminars[key] = []
        pairs_seminars[key].append(seminars)
    await message.answer(
        render_template("next_day.j2", {"pairs": pairs_seminars, "date": date}),
        parse_mode=formatter.PARSE_MODE,
    )
