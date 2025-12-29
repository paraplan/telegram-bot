from telegrinder import CALLBACK_QUERY_FOR_MESSAGE, Choice, Dispatch, Message
from telegrinder.rules import Command

from bot.client import wm
from bot.utils.nodes import DBRepository, UserSettingsDB

dp = Dispatch()


@dp.message(Command("subgroup"))
async def handle_subgroup(
    message: Message, user_settings: UserSettingsDB, repository: DBRepository
):
    choice = Choice(
        message="Выберите подгруппу",
        ready_text="Подтвердить👌",
        max_in_row=2,
        chat_id=message.chat.id,
        waiter_machine=wm,
    )
    choice.add_option("1", "1 подгруппа", "✅1 подгруппа", is_picked=user_settings.subgroup == 1)
    choice.add_option("2", "2 подгруппа", "✅2 подгруппа", is_picked=user_settings.subgroup == 2)
    chosen, choice_id = await choice.wait(CALLBACK_QUERY_FOR_MESSAGE, message.ctx_api)
    await repository.user_settings.update_subgroup(
        user_id=message.from_user.id, subgroup=int(chosen)
    )
    await message.edit(text="👥 Подгруппа изменена", message_id=choice_id)
