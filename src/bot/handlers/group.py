from telegrinder import CALLBACK_QUERY_FOR_MESSAGE, Choice, Dispatch, Message
from telegrinder.rules import Command

from src.bot.client import wm
from src.database import RepositoryFactory
from src.database.models import User

dp = Dispatch()


@dp.message(Command("group"))
async def handle_group(message: Message, user: User, repository: RepositoryFactory):
    groups = await repository.group.get_all()
    choice = Choice(
        message="Выберите группу",
        ready_text="Подтвердить👌",
        max_in_row=3,
        chat_id=message.chat.id,
        waiter_machine=wm,
    )
    user_group_id = user.group_id
    for index, group in enumerate(groups):
        is_picked = False
        if user_group_id:
            is_picked = user_group_id == group.id
        else:
            if index == 0:
                is_picked = True
        choice.add_option(str(group.id), f"{group.name}", f"✅{group.name}", is_picked=is_picked)
    chosen, choice_id = await choice.wait(CALLBACK_QUERY_FOR_MESSAGE, message.ctx_api)

    await repository.user.update_group(user_id=message.from_user.id, group_id=int(chosen))
    await repository.user_settings.update_subgroup(user_id=message.from_user.id, subgroup=1)
    text = (
        "👥 Группа изменена, а подгруппа сброшена до первой\n"
        "Чтобы изменить подгруппу, используйте /subgroup"
    )
    await message.edit(
        text=text,
        message_id=choice_id,
    )
