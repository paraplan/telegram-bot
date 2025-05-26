from loguru import logger
from telegrinder import CALLBACK_QUERY_FOR_MESSAGE, Choice, Dispatch, Message
from telegrinder.rules import Command

from src.bot.client import wm
from src.database import RepositoryFactory
from src.database.models import Group, User

dp = Dispatch()


@dp.message(Command("group"))
async def handle_group(message: Message, user: User, repository: RepositoryFactory):
    groups = await repository.group.get_all()
    if len(groups) == 0:
        await message.answer("🚫 Ошибка: Группы не найдены")
        logger.error("No groups found, perhaps the database is empty (daemon not running yet)?")
        return

    groups, _ = await choose_area(message, groups)
    groups, _ = await choose_course(message, groups)
    chosen, choice_id = await choose_group(message, groups, user)

    await repository.user.update_group(user_id=message.from_user.id, group_id=int(chosen))
    await repository.user_settings.update_subgroup(user_id=message.from_user.id, subgroup=1)
    text = (
        "👥 Группа изменена, а подгруппа сброшена до первой\n"
        "Чтобы изменить подгруппу, используйте /subgroup"
    )
    await message.edit(
        text=text,
        message_id=choice_id,
    )


async def choose_area(message: Message, groups: list[Group]) -> tuple[list[Group], int]:
    """Подменю выбора площадки"""
    DEFAULT_AREA = "ССО"
    choice_area = Choice(
        message="🏢 Выберите площадку",
        ready_text="Далее ➡️",
        max_in_row=2,
        chat_id=message.chat.id,
        waiter_machine=wm,
    )
    areas = sorted(set(map(lambda x: x.area_name, groups)))
    for area in areas:
        choice_area.add_option(area, f"{area}", f"✅{area}", is_picked=area == DEFAULT_AREA)
    chosen_area, choice_area_id = await choice_area.wait(
        CALLBACK_QUERY_FOR_MESSAGE, message.ctx_api
    )
    await message.ctx_api.delete_message(
        chat_id=message.chat.id,
        message_id=choice_area_id,
    )
    filtered_groups = list(filter(lambda x: x.area_name == chosen_area, groups))
    return filtered_groups, choice_area_id


async def choose_course(message: Message, groups: list[Group]) -> tuple[list[Group], int]:
    """Подменю выбора курса"""
    DEFAULT_COURSE = 1
    choice_course = Choice(
        message="🎓 Выберите курс",
        ready_text="Далее ➡️",
        max_in_row=4,
        chat_id=message.chat.id,
        waiter_machine=wm,
    )
    courses = sorted(set(map(lambda x: x.course, groups)))
    for course in courses:
        choice_course.add_option(
            course, f"{course}", f"✅{course}", is_picked=course == DEFAULT_COURSE
        )
    chosen_course, choice_course_id = await choice_course.wait(
        CALLBACK_QUERY_FOR_MESSAGE, message.ctx_api
    )
    await message.ctx_api.delete_message(
        chat_id=message.chat.id,
        message_id=choice_course_id,
    )
    filtered_groups = list(filter(lambda x: x.course == chosen_course, groups))
    return filtered_groups, choice_course_id


async def choose_group(message: Message, groups: list[Group], user: User) -> tuple[str, int]:
    """Подменю выбора группы"""
    group_choice = Choice(
        message="👥 Выберите группу",
        ready_text="Подтвердить👌",
        max_in_row=3,
        chat_id=message.chat.id,
        waiter_machine=wm,
    )
    group_ids = map(lambda x: x.id, groups)
    for index, group in enumerate(groups):
        is_picked = False
        if user.group_id and user.group_id in group_ids:
            is_picked = user.group_id == group.id
        else:
            if index == 0:
                is_picked = True
        group_choice.add_option(
            str(group.id), f"{group.name}", f"✅{group.name}", is_picked=is_picked
        )
    chosen, choice_id = await group_choice.wait(CALLBACK_QUERY_FOR_MESSAGE, message.ctx_api)
    return chosen, choice_id
