from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import expression


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    username: Mapped[str | None] = mapped_column(String(32), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    group_id: Mapped[int | None] = mapped_column(ForeignKey("group.id"))

    group: Mapped[Optional["Group"]] = relationship(back_populates="users")
    options: Mapped[list["UserOptions"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), unique=True)

    users: Mapped[list["User"]] = relationship(back_populates="group")
    study_days: Mapped[list["StudyDay"]] = relationship(back_populates="group")

    def __repr__(self) -> str:
        return f"Group(id={self.id!r}, name={self.name!r}"


class UserOptions(Base):
    __tablename__ = "user_options"

    id: Mapped[int] = mapped_column(BigInteger(), ForeignKey("user.id"), primary_key=True)
    has_notify: Mapped[bool] = mapped_column(server_default=expression.true())

    user: Mapped["User"] = relationship(back_populates="options")

    def __repr__(self) -> str:
        return f"UserOptions(id={self.id!r}, has_notify={self.has_notify!r})"


class StudyDay(Base):
    __tablename__ = "study_day"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    date: Mapped[datetime]

    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))

    group: Mapped[Optional["Group"]] = relationship(back_populates="study_days")

    def __repr__(self) -> str:
        return f"StudyDay(id={self.id!r}, date={self.date!r}, group_id={self.group_id!r})"
