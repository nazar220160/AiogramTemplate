from typing import Type

from src.database.models import BotChats
from src.database.repositories.base import BaseRepository
from src.database.repositories.bot_chats.reader import BotChatsReader
from src.database.repositories.bot_chats.writer import BotChatsWriter


class BotChatsRepository(BaseRepository[BotChats]):
    model: Type[BotChats] = BotChats

    @property
    def reader(self) -> BotChatsReader:
        return BotChatsReader(self)

    @property
    def writer(self) -> BotChatsWriter:
        return BotChatsWriter(self)
