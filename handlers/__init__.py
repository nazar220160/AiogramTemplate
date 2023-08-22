from aiogram import Dispatcher

from handlers.error import register_all_error_handlers
from handlers.main import register_all_main_handlers
from handlers.admin import register_all_admin_handlers


def register_start_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_all_main_handlers,
        register_all_admin_handlers,
        register_all_error_handlers
    )
    for handler in handlers:
        handler(dp)
