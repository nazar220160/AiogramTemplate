from datetime import datetime

import aiogram.types
from aiogram import Dispatcher, types, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import keyboards
import texts.admin
from misc.types import CallbackData as Cb
from database import db
from filters import IsAdmin
from misc.states import Admin
from misc.utils import pagination, can_delete_admin


async def admin(message: types.Message):
    await message.answer(texts.admin.start(len_users=len(db.get_all_users())), reply_markup=keyboards.inline.admin())


async def admin_callback(callback: types.CallbackQuery, state: FSMContext):
    data = Cb.extract(data=callback.data)
    if data.data == Cb.Admin.ross():
        await state.set_state(Admin.ross)
        await state.set_data({'message_id': callback.message.message_id})
        await callback.message.edit_text("<b>Отправьте сообщение для рассылки</b>",
                                         reply_markup=keyboards.inline.back_to_admin())
    elif data.data == Cb.Admin.main():
        await state.clear()
        await callback.message.delete()
        await callback.message.answer(texts.admin.start(len_users=len(db.get_all_users())),
                                      reply_markup=keyboards.inline.admin())
    elif data.data == Cb.Admin.confirm_ross():
        await ross(callback.message, user_id=callback.from_user.id)

    elif data.data == Cb.Admin.get_db():
        text_file = aiogram.types.input_file.FSInputFile(path='database/database.db',
                                                         filename=f"База данных {datetime.now().date()}.db")

        await callback.message.reply_document(document=text_file)

    elif data.data == Cb.Admin.get_admins():
        pag = pagination(list_pages=db.get_all_admins(), len_pages=6)
        reply_markup = keyboards.inline.admin_list(pag, owner_id=callback.from_user.id)
        await callback.message.edit_reply_markup(reply_markup=reply_markup)

    elif data.data == Cb.Admin.remove_admin():
        admin_info = db.get_user_by_id(id_user=int(data.args[0]))
        if can_delete_admin(is_admin=admin_info.is_admin, owner_id=callback.from_user.id, user_id=admin_info.user_id):
            db.remove_admin(user_id=admin_info.user_id)
        pag = pagination(list_pages=db.get_all_admins(), len_pages=6)
        reply_markup = keyboards.inline.admin_list(pag, owner_id=callback.from_user.id)
        await callback.message.edit_reply_markup(reply_markup=reply_markup)

    elif data.data == Cb.Admin.move_admins():
        page_num = int(data.args[0])
        pag = pagination(list_pages=db.get_all_admins(), len_pages=6)
        reply_markup = keyboards.inline.admin_list(pag, owner_id=callback.from_user.id, page_num=page_num)
        await callback.message.edit_reply_markup(reply_markup=reply_markup)


async def ross(message: types.Message, user_id: int):
    errors = []
    good = 0
    all_users = db.get_all_users()
    file_text = b''
    for i in all_users:
        if i.user_id == user_id:
            continue
        try:
            await message.copy_to(chat_id=i.user_id)
            file_text += bytes(f"{i.user_id}: Успешно!\n", 'utf-8')
            good += 1
        except Exception as e:
            errors.append(e)
            file_text += bytes(f"{i.user_id}: Ошибка! - {e}\n", 'utf-8')
    text_file = aiogram.types.input_file.BufferedInputFile(file_text,
                                                           filename=f"Рассылка сообщений {datetime.now().date()}.txt")

    await message.edit_reply_markup()
    await message.reply_document(document=text_file,
                                 caption=f'<b>Завершено. Успешно: {good}. Неудач: {len(errors)}</b>',
                                 reply_markup=keyboards.inline.back_to_admin())


async def get_ross_message(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await state.clear()
    await message.copy_to(chat_id=message.from_user.id, reply_markup=keyboards.inline.confirm_ross())
    await message.delete()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['message_id'])


async def send_money(message: types.Message):
    message_args = message.text.split()
    if len(message_args) < 3:
        await message.answer("Для отправки монет пользователя введите команду:\n"
                             "/send_money ID сумма")
    else:
        try:
            user_id = int(message_args[1])
            summ = float(message_args[2])
            db.add_balance(user_id=user_id, summ=summ)
            await message.answer(f"Успешно, баланс пользователя - {user_id} пополнен на {summ} $BBTCoin")
        except ValueError:
            await message.answer("ID и сумма должны состоять только из цифр")


async def add_admin(message: types.Message):
    message_args = message.text.split()
    if len(message_args) < 2:
        await message.answer("Для отправки монет пользователя введите команду:\n"
                             "/send_money ID сумма")

    else:
        try:
            user_id = int(message_args[1])
            db.add_admin(user_id=user_id, owner_id=message.from_user.id)
            await message.answer(f"Успешно")
        except ValueError:
            await message.answer("ID должен состоять только из цифр")


async def answer_the_question(message: types.Message):
    database_message = db.get_question(admin_message_id=message.reply_to_message.message_id)
    if database_message is None:
        await message.reply("Не найдено сообщение для ответа!")
        return
    if database_message.answered is True:
        await message.reply("Сообщение уже отвечено!")
        return
    try:
        await message.send_copy(chat_id=message.reply_to_message.forward_from.id,
                                reply_to_message_id=database_message.user_message_id)
    except TelegramBadRequest:
        await message.reply("Пользователь удалил сообщение либо заблокировал бота!")
        return
    except AttributeError:
        await message.reply("Ошибка!")
        return

    database_message.is_answer()
    await message.reply("Ответ отправлен!")


async def answer_photo_id(message: types.Message):
    photo_id = message.photo[-1].file_id
    await message.answer(photo_id)


async def answer_sticker_id(message: types.Message):
    sticker_id = message.sticker.file_id
    await message.answer(sticker_id)


def register_main_handlers(dp: Dispatcher):
    dp.message.register(admin, Command('admin'), IsAdmin())
    dp.callback_query.register(admin_callback, lambda c: Cb.extract(c.data, True).data == Cb.Admin(), IsAdmin())
    dp.message.register(get_ross_message, Admin.ross, IsAdmin())
    dp.message.register(send_money, Command('send_money'), IsAdmin())
    dp.message.register(add_admin, Command('add_admin'), IsAdmin())

    dp.message.register(answer_the_question, F.reply_to_message, IsAdmin())

    dp.message.register(answer_photo_id, F.photo, IsAdmin())
    dp.message.register(answer_sticker_id, F.sticker, IsAdmin())
