from aiogram import Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import keyboards
import texts.main
from database import db
from misc import states

from misc.types import CallbackData as Cb


async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=texts.main.start())


async def support(message: types.Message, state: FSMContext):
    await state.set_state(states.Support.message)
    await message.reply(text=texts.main.support(), reply_markup=keyboards.inline.support())


async def get_support_message(message: types.Message, state: FSMContext):
    await state.clear()
    mes = await message.forward(chat_id=db.get_all_admins()[0].user_id)
    db.add_question(user_message_id=message.message_id, admin_message_id=mes.message_id)
    await message.reply("Ваше сообщение отправлено администратору. Ожидайте ответа.")


async def back(callback: types.CallbackQuery, state: FSMContext):
    data = Cb.extract(callback.data)
    if data.data == Cb.Back.main_manu():
        await state.clear()
        await callback.message.delete()
        await callback.message.answer(texts.main.start())


def register_main_handlers(dp: Dispatcher):
    dp.message.register(start, CommandStart())
    dp.message.register(support, Command('support'))

    dp.callback_query.register(back, lambda c: Cb.extract(c.data, True).data == Cb.Back())

    dp.message.register(get_support_message, states.Support.message)
