from aiogram import Dispatcher

from telegram_bot.handlers.error import register_all_error_handlers
from telegram_bot.handlers.main import register_all_main_handlers
from telegram_bot.handlers.admin import register_all_admin_handlers
from telegram_bot.handlers.other import register_other_handlers


def register_start_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_all_main_handlers,
        register_all_admin_handlers,
        register_all_error_handlers,
        register_other_handlers
    )
    for handler in handlers:
        handler(dp)
