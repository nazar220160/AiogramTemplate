from typing import Optional

import redis.asyncio as aioredis
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from src.bot.core.models import MyBot
from src.core.config import Config


def load_storage(config: Config) -> BaseStorage:
    if not config.redis.dict:
        return MemoryStorage()
    try:
        storage = RedisStorage(redis=aioredis.Redis(**config.redis.dict))
    except ImportError:
        storage = MemoryStorage()
    return storage


def load_dispatcher(storage: Optional[BaseStorage] = None) -> Dispatcher:
    return Dispatcher(storage=storage)


def load_bot(config: Config) -> Bot:
    return MyBot(token=config.bot.token, parse_mode=ParseMode.HTML)
