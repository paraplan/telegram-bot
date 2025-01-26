from sqlalchemy import insert, select, update

from src.database.models import UserSettings
from src.database.repositories.abc import BaseRepository


class UserSettingsRepository(BaseRepository[UserSettings]):
    async def select_or_insert(self, user_id: int) -> UserSettings:
        select_statement = select(UserSettings).where(UserSettings.user_id == user_id)
        insert_statement = insert(UserSettings).values(user_id=user_id)
        return await self._process_insert_or_select(select_statement, insert_statement)

    async def _update_setting(self, user_id: int, **kwargs):
        statement = update(UserSettings).where(UserSettings.user_id == user_id).values(**kwargs)
        async with self.sessionmaker() as session:
            await session.execute(statement)
            await session.commit()

    async def update_subgroup(self, user_id: int, subgroup: int):
        await self._update_setting(user_id, subgroup=subgroup)
