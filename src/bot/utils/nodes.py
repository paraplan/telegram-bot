from loguru import logger
from telegrinder.node import NodeScope, UserId, scalar_node

from src.database.models import User, UserSettings
from src.database.repositories.factory import RepositoryFactory


@scalar_node(scope=NodeScope.GLOBAL)
class DBRepository:
    @classmethod
    def compose(cls) -> RepositoryFactory:
        logger.debug("Initializing repository factory")
        repository = RepositoryFactory()
        return repository


@scalar_node(scope=NodeScope.PER_CALL)
class UserDB:
    @classmethod
    async def compose(cls, user_id: UserId, db: DBRepository) -> User:
        logger.debug(f"Getting user from database for user id: {user_id}")
        return await db.user.select_or_insert(user_id)


@scalar_node(scope=NodeScope.PER_CALL)
class UserSettingsDB:
    @classmethod
    async def compose(cls, user_id: UserId, db: DBRepository) -> UserSettings:
        logger.debug(f"Getting user settings from database for user id: {user_id}")
        return await db.user_settings.select_or_insert(user_id)
