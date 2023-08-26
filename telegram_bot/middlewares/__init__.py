from aiogram import Dispatcher
from .main import DatabaseCheck


def register_all_middlewares(dp: Dispatcher):
    dp.message.middleware.register(DatabaseCheck())
    dp.callback_query.middleware.register(DatabaseCheck())
