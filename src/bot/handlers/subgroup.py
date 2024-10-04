from telegrinder import Choice, Dispatch, Message
from telegrinder.rules import Command

from src.bot.client import db_client, wm
from src.bot.utils.middlewares import MiddlewareType
from src.database.generated import update_user_subgroup

dp = Dispatch()


@dp.message(Command("subgroup"))
async def handle_subgroup(message: Message, user: MiddlewareType):
    choice = Choice(
        message="Выберите подгруппу",
        ready_text="Подтвердить👌",
        max_in_row=2,
        chat_id=message.chat.id,
        waiter_machine=wm,
    )
    choice.add_option("1", "1 подргруппа", "✅1 подгруппа", is_picked=user.default_subgroup == 1)
    choice.add_option("2", "2 подргруппа", "✅2 подгруппа", is_picked=user.default_subgroup == 2)
    chosen, choice_id = await choice.wait(message.ctx_api, dp.callback_query)
    await update_user_subgroup(db_client, sub_group=int(chosen), telegram_id=message.from_user.id)
    await message.edit(text="👥 Подгруппа изменена", message_id=choice_id)
