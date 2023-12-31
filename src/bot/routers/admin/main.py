from datetime import datetime
from typing import List

from aiogram import types, F
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot import keyboards
from src.bot.common.filters import IsAdmin
from src.bot.common.states.admin import Newsletter, ComChatCreator, BanUser
from src.bot.core.models import MyBot
from src.config.settings import Settings
from src.database.core import Database
from src.common.dto import UserDTO, UserUpdate, QuestionUpdate, ComSubChatsCreate, ComSubChatsUpdate
from src.bot.routers.admin.router import admin_router
from src.bot.utils.texts import admin as texts
from src.bot.utils.callback import CallbackData as Cb
from src.bot.utils.other import paginate
from src.utils.enums import Status
from src.bot.common.middlewares.i18n import gettext as _


@admin_router.message(Command('admin'), IsAdmin())
async def start(message: types.Message, db: Database):
    all_users = await db.user.select_many()
    await message.answer(_(texts.START).format(len_users=len(all_users)),
                         reply_markup=keyboards.admin())


@admin_router.callback_query(lambda c: Cb.extract(c.data, True).data == Cb.Admin())
async def admin_callback(callback: types.CallbackQuery, state: FSMContext, bot: MyBot, db: Database,
                         settings: Settings) -> None:
    data = Cb.extract(cd=callback.data)
    if data.data == Cb.Admin.ross():
        await state.set_state(Newsletter.message)
        await state.set_data({'message_id': callback.message.message_id})
        await callback.message.edit_text(_(texts.ENTER_MESSAGE_FOR_ROSS),
                                         reply_markup=keyboards.back(to=Cb.Admin.main()))
    elif data.data == Cb.Admin.main():
        await state.clear()
        await callback.message.delete()
        all_users = await db.user.select_many()
        await callback.message.answer(_(texts.START).format(len_users=len(all_users)),
                                      reply_markup=keyboards.admin())
    elif data.data == Cb.Admin.confirm_ross():
        list_users = await db.user.select_many()
        await ross(callback.message, user_id=callback.from_user.id, list_users=list_users)

    elif data.data == Cb.Admin.get_admins():
        list_admins = await db.user.get_admins()
        pag = paginate(list_items=list_admins, items_per_page=5)
        await callback.message.edit_reply_markup(reply_markup=keyboards.admin_list(ls=pag))

    elif data.data == Cb.Admin.com_sub():
        await callback.message.delete()
        list_chats = await db.com_sub_chats.select_many()
        pag = paginate(list_items=list_chats, items_per_page=5)
        await callback.message.answer(text=_(texts.ADMIN_PANEL_COM_SUB),
                                      reply_markup=keyboards.com_chats(ls=pag))

    elif data.data == Cb.Admin.add_com_chat():
        await callback.message.delete()
        await state.set_state(ComChatCreator.chat_id)
        bot_info = await bot.me()
        reply_markup = keyboards.add_com_chat(bot_username=bot_info.username)
        await callback.message.answer(_(texts.ADD_COM_CHAT), reply_markup=reply_markup)

    elif data.data == Cb.Admin.remove_com_chat():
        chat_id = int(data.args[0])
        list_chats = await db.com_sub_chats.delete(chat_id=chat_id)
        pag = paginate(list_items=list_chats, items_per_page=5)
        await callback.message.edit_reply_markup(reply_markup=keyboards.com_chats(ls=pag))

    elif data.data == Cb.Admin.move_com_chats():
        page_num = int(data.args[0])
        list_chats = await db.com_sub_chats.select_many()

        pag = paginate(list_items=list_chats, items_per_page=5)
        reply_markup = keyboards.com_chats(pag, page_num=page_num)
        await callback.message.edit_reply_markup(reply_markup=reply_markup)

    elif data.data == Cb.Admin.com_chat_toggle_turn():
        chat_id = int(data.args[0])

        chat_info = await db.com_sub_chats.select(chat_id=chat_id)
        list_chats = await db.com_sub_chats.update(
            chat_id=chat_id,
            query=ComSubChatsUpdate(
                turn=not chat_info.turn
            )
        )

        pag = paginate(list_items=list_chats, items_per_page=5)
        reply_markup = keyboards.com_chats(pag)
        await callback.message.edit_reply_markup(reply_markup=reply_markup)

    elif data.data == Cb.Admin.remove_admin():
        if callback.from_user.id not in settings.admins:
            await callback.answer(text=_(texts.INSUFFICIENT_PERMISSIONS), show_alert=True)
            return

        await db.user.update(user_id=int(data.args[0]), query=UserUpdate(admin=False))
        list_admins = await db.user.get_admins()

        pag = paginate(list_items=list_admins, items_per_page=5)
        await callback.message.edit_reply_markup(reply_markup=keyboards.admin_list(ls=pag))

    elif data.data == Cb.Admin.move_admins():
        page_num = int(data.args[0])
        list_admins = await db.user.get_admins()

        pag = paginate(list_items=list_admins, items_per_page=5)
        reply_markup = keyboards.admin_list(pag, page_num=page_num)
        await callback.message.edit_reply_markup(reply_markup=reply_markup)

    elif data.data == Cb.Admin.banned_users():
        list_banned_users = await db.user.get_blocked_users()
        pag = paginate(list_items=list_banned_users, items_per_page=5)
        await callback.message.delete()
        await callback.message.answer(
            text=_(texts.BANNED_USERS),
            reply_markup=keyboards.banned_users(ls=pag)
        )

    elif data.data == Cb.Admin.move_banned_users():
        page_num = int(data.args[0])
        list_banned_users = await db.user.get_blocked_users()
        pag = paginate(list_items=list_banned_users, items_per_page=5)
        reply_markup = keyboards.banned_users(ls=pag, page_num=page_num)
        await callback.message.edit_reply_markup(reply_markup=reply_markup)

    elif data.data == Cb.Admin.unban():
        user_id = int(data.args[0])

        await db.user.update(user_id=user_id, query=UserUpdate(
            blocked=False
        ))

        list_banned_users = await db.user.get_blocked_users()
        pag = paginate(list_items=list_banned_users, items_per_page=5)
        reply_markup = keyboards.banned_users(ls=pag)
        await callback.message.edit_reply_markup(reply_markup=reply_markup)
        await callback.answer(text=_(texts.SUCCESSFUL))

    elif data.data == Cb.Admin.ban():
        await callback.message.delete()
        await callback.message.answer(
            text=_(texts.SEND_USER_ID_TO_BAN),
            reply_markup=keyboards.back(to=Cb.Admin.main(), cancel=True)
        )
        await state.set_state(BanUser.user_id)


@admin_router.message(F.text, BanUser.user_id, IsAdmin())
async def get_user_id_ban_user(message: types.Message, db: Database, state: FSMContext):
    check_user = await db.user.select(user_id=message.text)
    if not check_user:
        await message.reply(_(texts.USER_NOT_FOUND), reply_markup=keyboards.back(to=Cb.Admin.main(), cancel=True))
        return

    await db.user.update(user_id=message.text, query=UserUpdate(
        blocked=True
    ))
    await message.reply(text=_(texts.BAN_USER_SUCCESSFUL).format(check_user.first_name),
                        reply_markup=keyboards.back(to=Cb.Admin.main(), main_menu=True))
    await state.clear()


async def ross(message: types.Message, user_id: int, list_users: List[UserDTO]):
    errors = []
    good = 0
    file_text = b''
    for i in list_users:
        if i.user_id == user_id:
            continue
        try:
            await message.copy_to(chat_id=i.user_id)
            file_text += bytes(f"{i.user_id}: {_(texts.SUCCESSFUL)}\n", 'utf-8')
            good += 1
        except Exception as e:
            errors.append(e)
            file_text += bytes(f"{i.user_id}: {_(texts.ERROR)} - {e}\n", 'utf-8')
    text_file = types.input_file.BufferedInputFile(file=file_text,
                                                   filename=_(texts.ROSS_FILE_NAME).format(
                                                       date=datetime.now().date()))

    await message.edit_reply_markup()
    if file_text:
        await message.reply_document(document=text_file,
                                     caption=_(texts.ROSS_DONE).format(good=good, errors=len(errors)),
                                     reply_markup=keyboards.back(to=Cb.Admin.main()))


@admin_router.message(Newsletter.message, IsAdmin())
async def get_ross_message(message: types.Message, state: FSMContext, bot: MyBot):
    data = await state.get_data()
    await state.clear()
    await message.copy_to(chat_id=message.from_user.id, reply_markup=keyboards.confirm_ross())
    await message.delete()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['message_id'])


@admin_router.message(Command('add_admin'), IsAdmin())
async def add_admin(message: types.Message, db: Database):
    message_args = message.text.split()
    if len(message_args) < 2:
        await message.answer(_(texts.FOR_SEND_MESSAGE_ENTER_COMMAND))

    else:
        try:
            user_id = int(message_args[1])
            await db.user.update(user_id=user_id, query=UserUpdate(admin=True))
            await message.answer(_(texts.SUCCESSFUL))
        except ValueError:
            await message.answer(_(texts.MUST_BE_INTEGER))


@admin_router.message(F.reply_to_message, IsAdmin())
async def answer_the_question(message: types.Message, db: Database):
    message_id = message.reply_to_message.message_id

    database_message = await db.question.select(admin_message_id=message_id)
    if database_message is None:
        await message.reply(_(texts.MESSAGE_NOT_FOUND))
        return
    if database_message.status == Status.SUCCESS:
        await message.reply(_(texts.MESSAGE_ALREADY_ANSWERED))
        return
    elif database_message.status == Status.IN_PROGRESS:
        await message.reply(_(texts.MESSAGE_ALREADY_ANSWERED))
        return
    try:
        await message.send_copy(chat_id=message.reply_to_message.forward_from.id,
                                reply_to_message_id=database_message.user_message_id)
    except TelegramBadRequest:
        await message.reply(_(texts.USER_BLOCKED_BOT_OR_DELETE_MESSAGE))
        return
    except AttributeError:
        await message.reply(_(texts.ERROR))
        return

    await db.question.update(admin_message_id=message_id, query=QuestionUpdate(answered=True))
    await message.reply(_(texts.REPLY_SEND))


@admin_router.message(ComChatCreator.chat_id, IsAdmin())
async def get_com_chat(message: types.Message, bot: MyBot, db: Database, state: FSMContext):
    back_kb = keyboards.back(to=Cb.Admin.main())
    if not message.forward_from_chat and not message.forward_from and message.text:
        try:
            chat_id = int(message.text)
        except ValueError:
            await message.answer(_(texts.MUST_BE_INTEGER), reply_markup=back_kb)
            return
    elif message.forward_from:
        await message.answer(_(texts.MESSAGE_MUST_BE_FORWARD_FROM_CHANNEL), reply_markup=back_kb)
        return
    elif message.forward_from_chat:
        chat_id = message.forward_from_chat.id
    else:
        await message.answer(_(texts.UNKNOWN_ERROR), reply_markup=back_kb)
        return

    try:
        bot_info = await bot.me()
        chat_info = await bot.get_chat(chat_id=chat_id)
        if chat_info.username is None:
            await message.answer(_(texts.GET_COM_CHAT_MUST_BE_PUBLIC), reply_markup=back_kb)
            return

        chat_db = await db.com_sub_chats.select(chat_id=chat_info.id)
        if chat_db is not None:
            await message.answer(_(texts.GET_COM_CHAT_ALREADY_IN_DB), reply_markup=back_kb)
            return

        bot_in_chat = await bot.get_chat_member(user_id=bot_info.id, chat_id=chat_id)
        if bot_in_chat.status != ChatMemberStatus.ADMINISTRATOR:
            await message.answer(_(texts.GET_COM_CHAT_NOT_ADMIN), reply_markup=back_kb)
            return

        await db.com_sub_chats.create(query=ComSubChatsCreate(
            chat_id=chat_info.id,
            username=chat_info.username
        ))

        await state.clear()

        list_chats = await db.com_sub_chats.select_many()
        pag = paginate(list_items=list_chats, items_per_page=5)
        all_users = await db.user.select_many()
        await message.answer(text=_(texts.START).format(len_users=len(all_users)),
                             reply_markup=keyboards.com_chats(ls=pag))

    except TelegramBadRequest:
        await message.answer(text=_(texts.GET_COM_CHAT_NOT_FOUND), reply_markup=back_kb)
        return


@admin_router.message(F.photo, IsAdmin())
async def answer_photo_id(message: types.Message):
    photo_id = message.photo[-1].file_id
    await message.answer(photo_id)


@admin_router.message(F.sticker, IsAdmin())
async def answer_sticker_id(message: types.Message):
    sticker_id = message.sticker.file_id
    await message.answer(sticker_id)
