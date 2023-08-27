from aiogram import Dispatcher, types
import telegram_bot.texts
from telegram_bot import keyboards
from telegram_bot.database import models


async def check_subs(callback: types.CallbackQuery, user_info: models.User):
    await callback.message.delete()
    reply_markup = keyboards.inline.start(is_admin=bool(user_info.is_admin))
    await callback.message.answer(text=telegram_bot.texts.main.start(),
                                  reply_markup=reply_markup)


def register_other_handlers(dp: Dispatcher):
    dp.callback_query.register(check_subs, lambda c: c.data == 'check_subs')
