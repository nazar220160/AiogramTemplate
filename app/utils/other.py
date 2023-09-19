import time
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


def can_delete_admin(owner_id: int, user_id: int, is_admin: int) -> bool:
    return is_admin == owner_id or user_id == owner_id


def get_next_pag(len_ls, page_num):
    move_back = len_ls - 1 if page_num == 0 else page_num - 1
    move_next = 0 if page_num == len_ls - 1 else page_num + 1
    return move_back, move_next
