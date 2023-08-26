from aiogram import Dispatcher, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter


async def telegram_bad_request(exception: types.ErrorEvent):
    if exception.update.callback_query:
        await exception.update.callback_query.answer(str(exception.exception),
                                                     show_alert=True)
    elif exception.update.message:
        await exception.update.message.reply(str(exception.exception))


async def connection_error(exception: types.ErrorEvent):
    if exception.update.callback_query:
        await exception.update.callback_query.answer(str(exception.exception),
                                                     show_alert=True)
    elif exception.update.message:
        await exception.update.message.reply(str(exception.exception))


def register_main_handlers(dp: Dispatcher):
    dp.errors.register(telegram_bad_request, ExceptionTypeFilter(TelegramBadRequest))
    dp.errors.register(connection_error, ExceptionTypeFilter(ConnectionError))
