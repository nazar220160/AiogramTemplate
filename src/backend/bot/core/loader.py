from typing import Optional

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage

from src.backend.bot.core.models import MyBot
from src.backend.config.settings import Settings
import redis.asyncio as aioredis


def load_storage(settings: Settings) -> BaseStorage:
    if not settings.redis_settings:
        return MemoryStorage()
    try:
        storage = RedisStorage(redis=aioredis.Redis(**settings.redis_settings))
    except ImportError:
        storage = MemoryStorage()
    return storage


def load_dispatcher(
        storage: Optional[BaseStorage] = None
) -> Dispatcher:
    return Dispatcher(storage=storage)


def load_bot(settings: Settings) -> Bot:
    return MyBot(
        token=settings.bot_token,
        parse_mode=ParseMode.HTML
    )
