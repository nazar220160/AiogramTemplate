from aiogram import Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import telegram_bot.texts.main
from telegram_bot import keyboards
from telegram_bot.database import base, models
from telegram_bot.misc import states

from telegram_bot.misc.types import CallbackData as Cb


async def start(message: types.Message, state: FSMContext, user_info: models.User):
    await state.clear()

    reply_markup = keyboards.inline.start(is_admin=bool(user_info.is_admin))

    await message.answer(text=telegram_bot.texts.main.start(),
                         reply_markup=reply_markup)


async def support(message: types.Message, state: FSMContext):
    await state.set_state(states.Support.message)
    await message.reply(text=telegram_bot.texts.main.support(), reply_markup=keyboards.inline.support())


async def get_support_message(message: types.Message, state: FSMContext):
    await state.clear()
    admin_list = await base.get_all_admins()
    mes = await message.forward(chat_id=admin_list[0].user_id)
    await base.add_question(user_message_id=message.message_id, admin_message_id=mes.message_id)
    await message.reply("Ваше сообщение отправлено администратору. Ожидайте ответа.")


async def back(callback: types.CallbackQuery, state: FSMContext, user_info: models.User):
    data = Cb.extract(callback.data)
    if data.data == Cb.Back.main_manu():
        await state.clear()
        await callback.message.delete()

        reply_markup = keyboards.inline.start(is_admin=bool(user_info.is_admin))

        await callback.message.answer(telegram_bot.texts.main.start(),
                                      reply_markup=reply_markup)


def register_main_handlers(dp: Dispatcher):
    dp.message.register(start, CommandStart())
    dp.message.register(support, Command('support'))

    dp.callback_query.register(back, lambda c: Cb.extract(c.data, True).data == Cb.Back())

    dp.message.register(get_support_message, states.Support.message)
