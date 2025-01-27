import datetime
from typing import List

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Time,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    subgroup: Mapped[int] = mapped_column(SmallInteger, server_default=func.text("1"))
    is_notify: Mapped[bool] = mapped_column(Boolean, server_default=func.text("true"))
    is_notify_vacation: Mapped[bool] = mapped_column(Boolean, server_default=func.text("true"))
    is_notify_practice: Mapped[bool] = mapped_column(Boolean, server_default=func.text("true"))
    is_notify_session: Mapped[bool] = mapped_column(Boolean, server_default=func.text("true"))

    # Relationships
    user: Mapped["User"] = relationship(back_populates="settings")


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    full_name: Mapped[str] = mapped_column(String)
    course: Mapped[int] = mapped_column(Integer)

    # Relationships
    users: Mapped[List["User"]] = relationship(back_populates="group")
    schedules: Mapped[List["Schedule"]] = relationship(back_populates="group")

    def __repr__(self):
        return f"Group(id={self.id}, full_name={self.full_name})"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    group_id: Mapped[int | None] = mapped_column(ForeignKey("group.id"), nullable=True)

    # Relationships
    group: Mapped[Group | None] = relationship(back_populates="users")
    settings: Mapped[UserSettings] = relationship(back_populates="user", uselist=False)

    def __repr__(self):
        return f"User(id={self.id}, group_id={self.group_id})"


class Room(Base):
    __tablename__ = "room"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_number: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    # Relationships
    lessons: Mapped[List["Lesson"]] = relationship(back_populates="room")

    def __repr__(self):
        return f"Room(id={self.id}, room_number={self.room_number})"


class Teacher(Base):
    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String)

    # Relationships
    lessons: Mapped[List["Lesson"]] = relationship(back_populates="teacher")

    def __repr__(self):
        return f"Teacher(id={self.id}, full_name={self.full_name})"


class Subject(Base):
    __tablename__ = "subject"
    __table_args__ = (UniqueConstraint("name", name="unique_subject_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    # Relationships
    lessons: Mapped[List["Lesson"]] = relationship(back_populates="subject")

    def __repr__(self):
        return f"Subject(id={self.id}, name={self.name})"


class DayType(Base):
    __tablename__ = "day_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    # Relationships
    time_slots: Mapped[List["TimeSlot"]] = relationship(back_populates="day_type")

    def __repr__(self):
        return f"DayType(id={self.id}, name={self.name})"


class TimeSlot(Base):
    __tablename__ = "time_slot"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day_type_id: Mapped[int] = mapped_column(ForeignKey("day_type.id"))
    start_time: Mapped[datetime.time] = mapped_column(Time)
    end_time: Mapped[datetime.time] = mapped_column(Time)
    lesson_number: Mapped[int] = mapped_column(SmallInteger)

    # Relationships
    day_type: Mapped[DayType] = relationship(back_populates="time_slots")
    lessons: Mapped[List["Lesson"]] = relationship(back_populates="time_slot")

    def __repr__(self):
        return f"TimeSlot(id={self.id}, start_time={self.start_time}, end_time={self.end_time})"


class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))
    date: Mapped[datetime.date] = mapped_column(Date)

    # Relationships
    group: Mapped[Group] = relationship(back_populates="schedules")
    lessons: Mapped[List["Lesson"]] = relationship(back_populates="schedule")

    def __repr__(self):
        return f"Schedule(id={self.id}, date={self.date})"


class Lesson(Base):
    __tablename__ = "lesson"
    __table_args__ = (
        UniqueConstraint("schedule_id", "time_slot_id", "subgroup", name="unique_lesson"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedule.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("teacher.id"), nullable=True)
    room_id: Mapped[int | None] = mapped_column(ForeignKey("room.id"), nullable=True)
    time_slot_id: Mapped[int] = mapped_column(ForeignKey("time_slot.id"))
    subgroup: Mapped[int] = mapped_column(SmallInteger)

    # Relationships
    schedule: Mapped[Schedule] = relationship(back_populates="lessons")
    subject: Mapped[Subject] = relationship(back_populates="lessons")
    teacher: Mapped[Teacher | None] = relationship(back_populates="lessons")
    room: Mapped[Room | None] = relationship(back_populates="lessons")
    time_slot: Mapped[TimeSlot] = relationship(back_populates="lessons")

    def __repr__(self):
        return f"Lesson(id={self.id}, schedule_id={self.schedule_id})"
