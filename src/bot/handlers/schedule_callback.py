import datetime

from telegrinder import CallbackQuery, Dispatch
from telegrinder.rules import CallbackDataJsonModel

from src.bot.client import formatter
from src.bot.utils.schedule import ScheduleCallbackData, render_schedule_for_date
from src.database import RepositoryFactory

dp = Dispatch()


@dp.callback_query(CallbackDataJsonModel(ScheduleCallbackData, alias="data"))
async def handle_subgroup(callback: CallbackQuery, data: ScheduleCallbackData):
    repository = RepositoryFactory()
    date = datetime.datetime.strptime(data.date, "%Y-%m-%d").date()
    group = await repository.group.get(data.group_id)
    text, keyboard = await render_schedule_for_date(
        repository, date, group, data.subgroup, data.is_week
    )
    await callback.edit_text(text=text, reply_markup=keyboard, parse_mode=formatter.PARSE_MODE)
