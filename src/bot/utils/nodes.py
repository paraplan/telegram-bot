from loguru import logger
from telegrinder.node import global_node, scalar_node
from telegrinder.node.nodes import UserId

from src.database.models import User, UserSettings
from src.database.repositories.factory import RepositoryFactory


@global_node
@scalar_node
class DBRepository:
    @classmethod
    def __compose__(cls) -> RepositoryFactory:
        logger.debug("Initializing repository factory")
        repository = RepositoryFactory()
        return repository


@scalar_node
class UserDB:
    @classmethod
    async def __compose__(cls, user_id: UserId, db: DBRepository) -> User:
        logger.debug(f"Getting user from database for user id: {user_id}")
        return await db.user.select_or_insert(user_id)


@scalar_node
class UserSettingsDB:
    @classmethod
    async def __compose__(cls, user_id: UserId, db: DBRepository) -> UserSettings:
        logger.debug(f"Getting user settings from database for user id: {user_id}")
        return await db.user_settings.select_or_insert(user_id)
