from telegrinder import ABCMiddleware, Context, Message

from src.env import LIST_ALLOWED_USERS


class AllowedUsersMiddleware(ABCMiddleware):
    async def pre(self, event: Message, ctx: Context) -> bool:
        if LIST_ALLOWED_USERS and event.chat.id not in LIST_ALLOWED_USERS:
            return False
        return True
