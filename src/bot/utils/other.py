from typing import List

from aiogram import Bot, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ChatMemberLeft

from src.database.models import BotChats


async def set_bot_commands(bot: Bot):
    commands = [
        types.BotCommand(command='/start', description='Bot start menu. Clears all the states'),
        types.BotCommand(command='/support', description='Bot tech support. ')
    ]
    await bot.set_my_commands(commands)


def get_next_pag(len_ls, page_num):
    move_back = len_ls - 1 if page_num == 0 else page_num - 1
    move_next = 0 if page_num == len_ls - 1 else page_num + 1
    return move_back, move_next


def paginate(list_items, items_per_page):
    paginated_list = []
    for i in range(0, len(list_items), items_per_page):
        page = list_items[i:i + items_per_page]
        paginated_list.append(page)
    return [[]] if not paginated_list else paginated_list


async def check_com_sub(
    bot: Bot, user_id: int, sub_list: List[BotChats]
) -> List[BotChats]:
    not_sub_list = []
    for chat in sub_list:
        if chat.permissions["status"] != "administrator":
            continue
        try:
            check = await bot.get_chat_member(chat_id=chat.id, user_id=user_id)
        except TelegramBadRequest:
            continue
        if isinstance(check, ChatMemberLeft):
            not_sub_list.append(chat)
    return not_sub_list
