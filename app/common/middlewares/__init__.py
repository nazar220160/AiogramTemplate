from typing import Optional
from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import AsyncEngine

from app.common.middlewares.add_user import AddUserMiddleware
from app.common.middlewares.database import DatabaseMiddleware
from app.common.middlewares.func import ComSubMiddleware
from app.common.middlewares.i18n import simple_locale_middleware


def register_middlewares(dp: Dispatcher, engine: Optional[AsyncEngine] = None) -> None:
    db_middleware = DatabaseMiddleware(engine)
    com_sub_middleware = ComSubMiddleware()
    add_user_middleware = AddUserMiddleware()

    simple_locale_middleware.setup(dp)

    dp.message.outer_middleware.register(db_middleware)
    dp.callback_query.outer_middleware.register(db_middleware)

    dp.message.middleware.register(add_user_middleware)
    dp.callback_query.middleware.register(add_user_middleware)

    dp.message.middleware.register(com_sub_middleware)
    dp.callback_query.middleware.register(com_sub_middleware)
