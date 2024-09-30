from telegrinder import ABCMiddleware, Context, Message

from src.bot.client import bot, db_client
from src.database.generated import InsertUserResult, insert_user

MiddlewareType = InsertUserResult


@bot.on.message.register_middleware()
class UserRegisterMiddleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: Context) -> bool:
        user = await insert_user(db_client, telegram_id=event.from_user.id)
        ctx.update({"user": user})
        return True
