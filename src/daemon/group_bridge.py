import datetime

from loguru import logger

from src.daemon.decorators import check_lesson_updates
from src.database import (
    GroupCreate,
    LessonCreate,
    RepositoryFactory,
    RoomCreate,
    ScheduleCreate,
    SubjectCreate,
)
from src.database.models import Group, Room, Schedule, Subject
from src.schedule_parser.area import AreaSchema
from src.schedule_parser.base import BaseItemSchema
from src.schedule_parser.group import GroupSchema
from src.schedule_parser.hours import HourSchema


@check_lesson_updates
async def process_group(
    repository: RepositoryFactory,
    area: AreaSchema,
    group: GroupSchema,
    schedule_date: datetime.date,
    time_slot_ids: dict[int, int],
) -> None:
    """Process group schedule and update database"""
    await create_group(repository, area, group)
    schedule_create = ScheduleCreate(group_id=group.info.id, date=schedule_date)
    schedule = await repository.schedule.select(schedule_create)
    # if schedule already exists process diff for hours
    # (delete lessons that are not in time_slot_ids)
    if schedule:
        await process_diff_for_hours(repository, group, schedule)
    else:
        schedule = await repository.schedule.create(schedule_create)
    await process_new_hours(repository, group, schedule.id, time_slot_ids)


async def process_diff_for_hours(
    repository: RepositoryFactory,
    group: GroupSchema,
    schedule: Schedule,
) -> None:
    existing_hours = await repository.lesson.get(group_id=group.info.id, date=schedule.date)
    subgroups = set(lesson.subgroup for lesson in existing_hours)
    logger.debug(f"Subgroups: {subgroups}")
    # if group has hours that has been deleted, delete them from database
    # for this we need to compare existing_hours with group.hours
    for subgroup in subgroups:
        existing_hours_numbers = set(
            lesson.time_slot.lesson_number
            for lesson in existing_hours
            if lesson.subgroup == subgroup
        )
        new_hours_numbers = set(
            hour_number
            for hour_number in group.hours.keys()
            if group.hours[hour_number].get(subgroup)
        )
        diff = existing_hours_numbers - new_hours_numbers
        if diff:
            logger.debug(f"Diff of hours: {diff}")
        for lesson in existing_hours:
            if lesson.time_slot.lesson_number in diff:
                await repository.lesson.delete(lesson.id)


async def process_new_hours(
    repository: RepositoryFactory,
    group: GroupSchema,
    schedule_id: int,
    time_slot_ids: dict[int, int],
) -> None:
    for hour_number, hour in group.hours.items():
        for sub_group_number, sub_group in hour.items():
            await process_lesson(
                repository=repository,
                schedule_id=schedule_id,
                sub_group=sub_group,
                time_slot_id=time_slot_ids[hour_number],
                sub_group_number=sub_group_number,
            )


async def process_lesson(
    repository: RepositoryFactory,
    sub_group: HourSchema,
    schedule_id: int,
    time_slot_id: int,
    sub_group_number: int,
) -> None:
    cabinet_id = (await create_room(repository, sub_group.room)).id if sub_group.room else None
    subject = await create_subject(repository, sub_group.occupation)
    lesson_create = LessonCreate(
        schedule_id=schedule_id,
        subject_id=subject.id,
        teacher_id=None,  # TODO
        room_id=cabinet_id,
        time_slot_id=time_slot_id,
        subgroup=sub_group_number,
    )
    await repository.lesson.merge(lesson_create)


async def create_group(
    repository: RepositoryFactory, area: AreaSchema, group: GroupSchema
) -> Group:
    group_create = GroupCreate(
        id=group.info.id,
        name=group.info.name,
        full_name=group.info.full_name,
        course=group.course,
        area_name=area.info.name,
    )
    created_group = await repository.group.insert_or_update(group_create, join_students=True)
    return created_group


async def create_subject(repository: RepositoryFactory, subject_name: str) -> Subject:
    """Create or update subject and return its ID"""
    subject_create = SubjectCreate(name=subject_name)
    created_subject = await repository.subject.insert_or_update(subject_create)
    return created_subject


async def create_room(repository: RepositoryFactory, cabinet: BaseItemSchema) -> Room:
    """Create or update cabinet and return its ID"""
    cabinet_create = RoomCreate(
        id=cabinet.id,
        room_number=cabinet.name,
        description=cabinet.full_name,
    )
    created_cabinet = await repository.room.insert_or_update(cabinet_create)
    return created_cabinet
