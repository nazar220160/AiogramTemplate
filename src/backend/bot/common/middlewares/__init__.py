from typing import Optional
from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import AsyncEngine

from src.backend.bot.common.middlewares.add_user import AddUserMiddleware
from src.backend.bot.common.middlewares.database import DatabaseMiddleware
from src.backend.bot.common.middlewares.func import ComSubMiddleware
from src.backend.bot.common.middlewares.i18n import simple_locale_middleware
from src.backend.config import load_settings


def register_middlewares(dp: Dispatcher, engine: Optional[AsyncEngine] = None) -> None:
    db_middleware = DatabaseMiddleware(db_url=load_settings().db_url, engine=engine)
    com_sub_middleware = ComSubMiddleware()
    add_user_middleware = AddUserMiddleware()

    simple_locale_middleware.setup(dp)

    dp.message.outer_middleware.register(db_middleware)
    dp.callback_query.outer_middleware.register(db_middleware)

    dp.message.middleware.register(add_user_middleware)
    dp.callback_query.middleware.register(add_user_middleware)

    dp.message.middleware.register(com_sub_middleware)
    dp.callback_query.middleware.register(com_sub_middleware)
