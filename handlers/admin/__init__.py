from aiogram import Dispatcher

from handlers.admin.main import register_main_handlers


def register_all_admin_handlers(dp: Dispatcher):
    handlers = (
        register_main_handlers,
    )
    for handler in handlers:
        handler(dp)
