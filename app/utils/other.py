import time
from typing import Iterator

from aiogram import Bot, types


class AutoExpireList:
    def __init__(self):
        self.data = []

    def add_item(self, item, expiration_time):
        self.data.append((item, time.time() + expiration_time))

    def get_items(self, expiration: bool = False):
        current_time = time.time()
        self.data = [(item, expiration) for item, expiration in self.data if expiration > current_time]
        if expiration is True:
            return [item for item in self.data]
        else:
            return [item[0] for item in self.data]


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