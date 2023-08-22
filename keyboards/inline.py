from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from database.databases import User
from config import sub_list
from misc.types import CallbackData as Cb
from misc.utils import can_delete_admin, get_next_pag


def admin():
    result = InlineKeyboardBuilder()
    result.row(InlineKeyboardButton(text="Рассылка",
                                    callback_data=Cb.Admin.ross()))
    result.add(InlineKeyboardButton(text="Админы",
                                    callback_data=Cb.Admin.get_admins()))
    result.row(InlineKeyboardButton(text="Получить базу данных",
                                    callback_data=Cb.Admin.get_db()))
    return result.as_markup()


def admin_list(ls: list[list[User]], owner_id: int, page_num=0):
    result = InlineKeyboardBuilder()
    len_ls = len(ls)
    count = page_num if len_ls != 1 else 0
    for i in ls[count]:
        callback_data = Cb.Admin.remove_admin(i.id)
        text_admin = f"{i.first_name} {i.last_name if i.last_name is not None else ''}"
        result.row(InlineKeyboardButton(text=text_admin, callback_data='None'))
        if can_delete_admin(owner_id=owner_id, user_id=i.user_id, is_admin=i.is_admin):
            result.add(InlineKeyboardButton(text="Удалить", callback_data=callback_data))
    if len(ls) != 1:
        move_back, move_next = get_next_pag(len_ls=len_ls, page_num=page_num)

        callback_data_back = Cb.Admin.move_admins(move_back)
        callback_data_next = Cb.Admin.move_admins(move_next)

        result.row(InlineKeyboardButton(text=f"⬅️", callback_data=callback_data_back))
        result.add(InlineKeyboardButton(text=f"{page_num + 1}/{len_ls}", callback_data=f"None"))
        result.add(InlineKeyboardButton(text=f"➡", callback_data=callback_data_next))

    result.row(InlineKeyboardButton(text="Назад", callback_data=Cb.Admin.main()))
    return result.as_markup()


def back_to_admin():
    result = InlineKeyboardBuilder()
    result.row(InlineKeyboardButton(text="Назад", callback_data=Cb.Admin.main()))
    return result.as_markup()


def confirm_ross():
    result = InlineKeyboardBuilder()
    confirm = InlineKeyboardButton(text="Подтвердить", callback_data=Cb.Admin.confirm_ross())
    cancel = InlineKeyboardButton(text="Отменить", callback_data=Cb.Admin.main())
    result.row(confirm).add(cancel)
    return result.as_markup()


def subscribe_chats(chat_list):
    result = InlineKeyboardBuilder()
    for chat_id in chat_list:
        link = sub_list[chat_id]['link']
        name = sub_list[chat_id]['name']
        result.row(InlineKeyboardButton(text=name, url=link))
    result.row(InlineKeyboardButton(text="Проверить", callback_data="check_subs"))
    return result.as_markup()
