from aiogram import Dispatcher
from .main import DatabaseCheck, CheckSubscribe


def register_all_middlewares(dp: Dispatcher):
    dp.message.middleware.register(DatabaseCheck())
    dp.callback_query.middleware.register(DatabaseCheck())
    dp.message.middleware.register(CheckSubscribe())
    dp.callback_query.middleware.register(CheckSubscribe())
