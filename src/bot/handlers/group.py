from uuid import UUID

from telegrinder import Choice, Dispatch, Message
from telegrinder.rules import Command

from src.bot.client import db_client, wm
from src.bot.utils.middlewares import MiddlewareType
from src.database.generated import get_all_groups, update_user_group, update_user_subgroup

dp = Dispatch()


@dp.message(Command("group"))
async def handle_group(message: Message, user: MiddlewareType):
    groups = await get_all_groups(db_client)
    choice = Choice(
        message="Выберите группу",
        ready_text="Подтвердить👌",
        max_in_row=3,
        chat_id=message.chat.id,
        waiter_machine=wm,
    )
    for index, group in enumerate(groups):
        is_picked: bool = False
        if user.group:
            if group.id == user.group.id:
                is_picked = True
        else:
            if index == 0:
                is_picked = True
        choice.add_option(str(group.id), f"{group.name}", f"✅{group.name}", is_picked=is_picked)
    chosen, choice_id = await choice.wait(message.ctx_api, dp.callback_query)

    await update_user_group(db_client, group_id=UUID(chosen), telegram_id=message.from_user.id)
    await update_user_subgroup(db_client, sub_group=1, telegram_id=message.from_user.id)
    await message.edit(
        text="👥 Группа изменена\nЧтобы изменить подгруппу, используйте /subgroup",
        message_id=choice_id,
    )
