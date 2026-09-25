from telegrinder import ABCMiddleware, Context, Message

from src.env import LIST_ALLOWED_USERS


class AllowedUsersMiddleware(ABCMiddleware):
    async def pre(self, event: Message, ctx: Context) -> bool:
        return not LIST_ALLOWED_USERS or event.chat.id in LIST_ALLOWED_USERS
