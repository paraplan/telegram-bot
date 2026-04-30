from telegrinder import Dispatch, Message
from telegrinder.rules import Command

from src.bot.utils.nodes import DBRepository, UserSettingsDB

dp = Dispatch()


@dp.message(Command("notifications"))
async def handle_notifications(
    message: Message, user_settings: UserSettingsDB, repository: DBRepository
):
    checkbox = dp.checkbox(
        message="⚙️ Настройки уведомлений",
        ready_text="⚙️ Сохранить",
        max_in_row=2,
        chat_id=message.chat.id,
    )

    checkbox.add_option(
        "is_notify",
        "🔔 Уведомления ❌",
        "🔔 Уведомления ✅",
        is_picked=user_settings.is_notify,
    )
    checkbox.add_option(
        "is_notify_vacation",
        "🏖️ Каникулы ❌",
        "🏖️ Каникулы ✅",
        is_picked=user_settings.is_notify_vacation,
    )
    checkbox.add_option(
        "is_notify_practice",
        "💻 Практика ❌",
        "💻 Практика ✅",
        is_picked=user_settings.is_notify_practice,
    )
    checkbox.add_option(
        "is_notify_session",
        "📚 Сессия ❌",
        "📚 Сессия ✅",
        is_picked=user_settings.is_notify_session,
    )

    chosen, choice_id = await checkbox.wait(message.api)

    for key, value in chosen.items():
        params = {key: bool(value)}
        await repository.user_settings._update_setting(user_id=message.from_user.id, **params)

    await message.edit(
        text="⚙️ Настройки обновлены",
        message_id=choice_id,
    )
