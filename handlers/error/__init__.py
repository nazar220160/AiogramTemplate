from aiogram import Dispatcher

from config import DEBUG
from handlers.error.error import register_main_handlers


def register_all_error_handlers(dp: Dispatcher):
    if DEBUG is False:
        handlers = (
            register_main_handlers,
        )
        for handler in handlers:
            handler(dp)
