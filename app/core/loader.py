from typing import Optional

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from app.core.settings import Settings
import redis.asyncio as aioredis


def load_storage(settings: Settings) -> BaseStorage:
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
    return Bot(
        token=settings.bot_token,
        parse_mode=settings.parse_mode,
        disable_web_page_preview=settings.disable_web_page_preview,
    )