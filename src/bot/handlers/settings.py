from telegrinder import Checkbox, Dispatch, Message
from telegrinder.rules import Command

from src.bot.client import wm
from src.database import RepositoryFactory
from src.database.models import User, UserSettings

dp = Dispatch()


@dp.message(Command("settings"))
async def handle_settings(
    message: Message, user: User, user_settings: UserSettings, repository: RepositoryFactory
):
    choice = Checkbox(
        message="⚙️ Настройки уведомлений",
        ready_text="⚙️ Сохранить",
        max_in_row=2,
        chat_id=message.chat.id,
        waiter_machine=wm,
    )

    choice.add_option(
        "is_notify",
        "🔔 Уведомления ❌",
        "🔔 Уведомления ✅",
        is_picked=user_settings.is_notify,
    )
    choice.add_option(
        "is_notify_vacation",
        "🏖️ Каникулы ❌",
        "🏖️ Каникулы ✅",
        is_picked=user_settings.is_notify_vacation,
    )
    choice.add_option(
        "is_notify_practice",
        "💻 Практика ❌",
        "💻 Практика ✅",
        is_picked=user_settings.is_notify_practice,
    )
    choice.add_option(
        "is_notify_session",
        "📚 Сессия ❌",
        "📚 Сессия ✅",
        is_picked=user_settings.is_notify_session,
    )

    chosen, choice_id = await choice.wait(message.ctx_api, dp.callback_query)

    for key, value in chosen.items():
        params = {key: bool(value)}
        await repository.user_settings._update_setting(user_id=message.from_user.id, **params)

    await message.edit(
        text="⚙️ Настройки обновлены",
        message_id=choice_id,
    )
