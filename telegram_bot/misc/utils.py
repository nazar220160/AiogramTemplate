import asyncio
import datetime
import time

from aiogram import Bot, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ChatMemberLeft

from html.parser import HTMLParser


def pagination(list_pages: list, len_pages: int):
    p = 0
    pag = []
    page = []
    for i in list_pages:
        if p > len_pages:
            pag.append(page)
            page = []
            p = 0
        page.append(i)
        p += 1
    pag.append(page)
    return pag


def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now
    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        return dt


def extract_unique_code(text) -> str:
    return text.split()[1] if len(text.split()) > 1 else None


async def check_sub(bot: Bot, user_id: int, sub_list):
    not_sub_list = []
    for chat in sub_list:
        try:
            check = await bot.get_chat_member(chat_id=chat, user_id=user_id)
        except TelegramBadRequest:
            continue
        if isinstance(check, ChatMemberLeft):
            not_sub_list.append(chat)
    return not_sub_list


def get_user_tasks(user_id) -> list[asyncio.Task]:
    tasks = []
    for i in asyncio.all_tasks():
        if str(i.get_name().split("~")[0]) == str(user_id):
            tasks.append(i)

    return tasks


async def set_bot_commands(bot: Bot, bot_commands):
    result = [types.BotCommand(command=i['command'], description=i['description']) for i in bot_commands]
    await bot.set_my_commands(result)


def can_delete_admin(owner_id: int, user_id: int, is_admin: int) -> bool:
    return is_admin == owner_id or user_id == owner_id


def parse_html_tags(text):
    class TagCounter(HTMLParser):
        def __init__(self):
            super().__init__()
            self.open_tags = []
            self.closed_tags = []

        def handle_starttag(self, tag, attrs):
            self.open_tags.append(tag)

        def handle_endtag(self, tag):
            self.closed_tags.append(tag)

    parser = TagCounter()
    parser.feed(text)

    open_tag_count = parser.open_tags
    closed_tag_count = parser.closed_tags
    unique_tags = set(parser.open_tags + parser.closed_tags)

    return open_tag_count, closed_tag_count, unique_tags


def split_html_text(text, chunk_size=4096):
    chunks = []
    open_tag_nex = None

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        if open_tag_nex is not None:
            chunk = f"<{open_tag_nex}>" + chunk
            open_tag_nex = None
        open_tags, closed_tags, unique_tags = parse_html_tags(chunk)
        if len(open_tags) > len(closed_tags):
            chunk += f"</{open_tags[-1]}>"
            open_tag_nex = open_tags[-1]

        chunks.append(chunk)

    return chunks


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


def get_next_pag(len_ls, page_num):
    move_back = len_ls - 1 if page_num == 0 else page_num - 1
    move_next = 0 if page_num == len_ls - 1 else page_num + 1
    return move_back, move_next
