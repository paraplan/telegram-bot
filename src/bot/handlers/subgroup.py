from telegrinder import CALLBACK_QUERY_FOR_MESSAGE, Choice, Dispatch, Message
from telegrinder.rules import Command

from src.bot.client import wm
from src.database import RepositoryFactory
from src.database.models import User, UserSettings

dp = Dispatch()


@dp.message(Command("subgroup"))
async def handle_subgroup(
    message: Message, user: User, user_settings: UserSettings, repository: RepositoryFactory
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
