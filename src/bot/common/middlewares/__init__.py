from typing import Optional
from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from sqlalchemy.ext.asyncio import AsyncEngine

from src.bot.common.middlewares.add_user import AddUserMiddleware
from src.bot.common.middlewares.ban import BanMiddleware
from src.bot.common.middlewares.database import DatabaseMiddleware
from src.bot.common.middlewares.func import ComSubMiddleware
from src.bot.common.middlewares.i18n import simple_locale_middleware
from src.bot.common.middlewares.throttle import ThrottlingMiddleware
from src.config import load_settings


def register_middlewares(dp: Dispatcher, engine: Optional[AsyncEngine] = None) -> None:
    db_middleware = DatabaseMiddleware(db_url=load_settings().db_url, engine=engine)
    com_sub_middleware = ComSubMiddleware()
    add_user_middleware = AddUserMiddleware()
    ban_middleware = BanMiddleware()
    throttling_middleware = ThrottlingMiddleware(storage=dp.storage)

    simple_locale_middleware.setup(dp)

    dp.message.outer_middleware.register(throttling_middleware)

    dp.message.outer_middleware.register(db_middleware)
    dp.callback_query.outer_middleware.register(db_middleware)

    dp.message.middleware.register(add_user_middleware)
    dp.callback_query.middleware.register(add_user_middleware)

    dp.message.middleware.register(ban_middleware)
    dp.callback_query.middleware.register(ban_middleware)

    dp.message.middleware.register(com_sub_middleware)
    dp.callback_query.middleware.register(com_sub_middleware)
