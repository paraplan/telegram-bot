from telegrinder import ABCMiddleware, Context, Message

from src.database import RepositoryFactory
from src.env import LIST_ALLOWED_USERS


class AllowedUsersMiddleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: Context) -> bool:
        if LIST_ALLOWED_USERS and event.chat.id not in LIST_ALLOWED_USERS:
            return False
        return True


class UserRegisterMiddleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: Context) -> bool:
        repository = RepositoryFactory()
        user = await repository.user.select_or_insert(event.from_user.id)
        user_settings = await repository.user_settings.select_or_insert(event.from_user.id)
        ctx.update({"user": user, "user_settings": user_settings, "repository": repository})
        return True
