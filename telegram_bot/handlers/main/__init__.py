from aiogram import Dispatcher

from telegram_bot.handlers.main.main import register_main_handlers


def register_all_main_handlers(dp: Dispatcher):
    handlers = (
        register_main_handlers,
    )
    for handler in handlers:
        handler(dp)
