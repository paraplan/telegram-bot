from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload

from src.database.models import Group, User, UserSettings
from src.database.repositories.abc import BaseRepository
from src.database.schemas import ScheduleType


class UserRepository(BaseRepository[User]):
    async def select_or_insert(self, id: int) -> User:
        select_statement = (
            select(User)
            .where(User.id == id)
            .options(selectinload(User.group), selectinload(User.settings))
        )
        insert_statement = insert(User).values(id=id)
        return await self._process_insert_or_select(select_statement, insert_statement)

    async def update_group(self, user_id: int, group_id: int):
        statement = update(User).where(User.id == user_id).values(group_id=group_id)
        async with self.sessionmaker() as session:
            await session.execute(statement)
            await session.commit()

    async def get_by_settings(
        self,
        group_id: int,
        schedule_type: ScheduleType,
    ):
        statement = (
            select(User)
            .join(UserSettings)
            .join(Group)
            .where(UserSettings.is_notify, Group.id == group_id)
        )
        if schedule_type == ScheduleType.VACATION:
            statement = statement.where(UserSettings.is_notify_vacation)
        elif schedule_type == ScheduleType.PRACTICE:
            statement = statement.where(UserSettings.is_notify_practice)
        elif schedule_type == ScheduleType.SESSION:
            statement = statement.where(UserSettings.is_notify_session)
        async with self.sessionmaker() as session:
            result = await session.execute(statement)
        return result.scalars().all()
