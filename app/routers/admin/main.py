from datetime import datetime
from typing import List

import aiogram.types
from aiogram import types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import app.utils.texts.admin
from app import keyboards
from app.common.filters import IsAdmin
from app.common.states.admin import Newsletter
from app.core.models import MyBot
from app.core.settings import Settings
from app.database.core import Database
from app.database.dto import UserDTO, UserUpdate, QuestionUpdate
from app.routers.admin.router import admin_router
from app.utils.callback import CallbackData as Cb
from app.utils.other import paginate


@admin_router.message(Command('admin'), IsAdmin())
async def start(message: types.Message, db: Database):
    all_users = await db.user.select_many()
    await message.answer(app.utils.texts.admin.start(len_users=len(all_users)),
                         reply_markup=keyboards.inline.admin())


@admin_router.callback_query(lambda c: Cb.extract(c.data, True).data == Cb.Admin(), IsAdmin())
async def admin_callback(callback: types.CallbackQuery, state: FSMContext, db: Database, settings: Settings) -> None:
    data = Cb.extract(cd=callback.data)
    if data.data == Cb.Admin.ross():
        await state.set_state(Newsletter.message)
        await state.set_data({'message_id': callback.message.message_id})
        await callback.message.edit_text("<b>Отправьте сообщение для рассылки</b>",
                                         reply_markup=app.keyboards.inline.back_to_admin())
    elif data.data == Cb.Admin.main():
        await state.clear()
        await callback.message.delete()
        all_users = await db.user.select_many()
        await callback.message.answer(app.utils.texts.admin.start(len_users=len(all_users)),
                                      reply_markup=app.keyboards.inline.admin())
    elif data.data == Cb.Admin.confirm_ross():
        list_users = await db.user.select_many()
        await ross(callback.message, user_id=callback.from_user.id, list_users=list_users)

    elif data.data == Cb.Admin.get_admins():
        list_admins = await db.user.get_admins()
        pag = paginate(list_items=list_admins, items_per_page=5)
        await callback.message.edit_reply_markup(reply_markup=keyboards.inline.admin_list(ls=pag))

    elif data.data == Cb.Admin.remove_admin():
        if callback.from_user.id not in settings.admins:
            await callback.answer(text="Недостаточно прав!", show_alert=True)
            return

        await db.user.update(user_id=int(data.args[0]), query=UserUpdate(admin=False))
        list_admins = await db.user.get_admins()

        pag = paginate(list_items=list_admins, items_per_page=5)
        await callback.message.edit_reply_markup(reply_markup=keyboards.inline.admin_list(ls=pag))

    elif data.data == Cb.Admin.move_admins():
        page_num = int(data.args[0])
        list_admins = await db.user.get_admins()

        pag = paginate(list_items=list_admins, items_per_page=5)
        reply_markup = app.keyboards.inline.admin_list(pag, page_num=page_num)
        await callback.message.edit_reply_markup(reply_markup=reply_markup)


async def ross(message: types.Message, user_id: int, list_users: List[UserDTO]):
    errors = []
    good = 0
    file_text = b''
    for i in list_users:
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
                                 reply_markup=app.keyboards.inline.back_to_admin())


@admin_router.message(Newsletter.message, IsAdmin())
async def get_ross_message(message: types.Message, state: FSMContext, bot: MyBot):
    data = await state.get_data()
    await state.clear()
    await message.copy_to(chat_id=message.from_user.id, reply_markup=app.keyboards.inline.confirm_ross())
    await message.delete()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['message_id'])


@admin_router.message(Command('add_admin'), IsAdmin())
async def add_admin(message: types.Message, db: Database):
    message_args = message.text.split()
    if len(message_args) < 2:
        await message.answer("Для отправки монет пользователя введите команду:\n"
                             "/send_money ID сумма")

    else:
        try:
            user_id = int(message_args[1])
            await db.user.update(user_id=user_id, query=UserUpdate(admin=True))
            await message.answer(f"Успешно")
        except ValueError:
            await message.answer("ID должен состоять только из цифр")


@admin_router.message(F.reply_to_message, IsAdmin())
async def answer_the_question(message: types.Message, db: Database):
    message_id = message.reply_to_message.message_id

    database_message = await db.question.select(admin_message_id=message_id)
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

    await db.question.update(admin_message_id=message_id, query=QuestionUpdate(answered=True))
    await message.reply("Ответ отправлен!")


@admin_router.message(F.photo, IsAdmin())
async def answer_photo_id(message: types.Message):
    photo_id = message.photo[-1].file_id
    await message.answer(photo_id)


@admin_router.message(F.sticker, IsAdmin())
async def answer_sticker_id(message: types.Message):
    sticker_id = message.sticker.file_id
    await message.answer(sticker_id)
