from aiogram import Dispatcher

from src.bot.common.middlewares.add_user import AddUserMiddleware
from src.bot.common.middlewares.ban import BanMiddleware
from src.bot.common.middlewares.database import DatabaseMiddleware
from src.bot.common.middlewares.func import ComSubMiddleware
from src.bot.common.middlewares.i18n import simple_locale_middleware
from src.bot.common.middlewares.throttle import ThrottlingMiddleware
from src.database.core.connection import SessionFactoryType


def register_middlewares(dp: Dispatcher, session_factory: SessionFactoryType) -> None:
    db_middleware = DatabaseMiddleware(session_factory)
    com_sub_middleware = ComSubMiddleware()
    add_user_middleware = AddUserMiddleware()
    ban_middleware = BanMiddleware()
    throttling_middleware = ThrottlingMiddleware(storage=dp.storage)

    simple_locale_middleware.setup(dp)

    dp.message.outer_middleware.register(throttling_middleware)

    dp.message.outer_middleware.register(db_middleware)
    dp.callback_query.outer_middleware.register(db_middleware)
    dp.my_chat_member.outer_middleware.register(db_middleware)

    dp.message.middleware.register(add_user_middleware)
    dp.callback_query.middleware.register(add_user_middleware)

    dp.message.middleware.register(ban_middleware)
    dp.callback_query.middleware.register(ban_middleware)

    dp.message.middleware.register(com_sub_middleware)
    dp.callback_query.middleware.register(com_sub_middleware)
