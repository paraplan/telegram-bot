from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload

from src.database.models import Group, User, UserSettings
from src.database.repositories.abc import BaseRepository


class UserRepository(BaseRepository[User]):
    async def select_or_insert(self, id: int) -> User:
        statement = (
            insert(User)
            .values(id=id)
            .on_conflict_do_update(
                index_elements=["id"],
                set_=dict(id=id),
            )
            .returning(User)
            .options(selectinload(User.group), selectinload(User.settings))
        )
        result = await self._execute(statement, commit=True)
        return result.scalar_one()

    async def update_group(self, user_id: int, group_id: int):
        statement = update(User).where(User.id == user_id).values(group_id=group_id)
        async with self.sessionmaker() as session:
            await session.execute(statement)
            await session.commit()

    async def get_by_settings(
        self,
        group_id: int,
        is_notify: bool,
        is_notify_vacation: bool | None = None,
        is_notify_practice: bool | None = None,
        is_notify_session: bool | None = None,
    ):
        statement = (
            select(User)
            .join(UserSettings)
            .join(Group)
            .where(UserSettings.is_notify == is_notify, Group.id == group_id)
        )
        if is_notify_vacation is not None:
            statement = statement.where(UserSettings.is_notify_vacation == is_notify_vacation)
        if is_notify_practice is not None:
            statement = statement.where(UserSettings.is_notify_practice == is_notify_practice)
        if is_notify_session is not None:
            statement = statement.where(UserSettings.is_notify_session == is_notify_session)
        async with self.sessionmaker() as session:
            result = await session.execute(statement)
        return result.scalars().all()
