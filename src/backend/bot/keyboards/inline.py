from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from src.backend.common.dto import UserDTO, ComSubChatsDTO
from src.backend.bot.utils.callback import CallbackData as Cd
from src.backend.bot.utils.other import get_next_pag

from src.backend.bot.utils.texts import buttons as texts


def start():
    result = InlineKeyboardBuilder()
    return result.as_markup()


def admin():
    result = InlineKeyboardBuilder()
    result.row(InlineKeyboardButton(text=f"📢 {texts.NEWSLETTER}", callback_data=Cd.Admin.ross()))
    result.add(InlineKeyboardButton(text=f"👥 {texts.ADMINS}", callback_data=Cd.Admin.get_admins()))
    result.row(InlineKeyboardButton(text=f"💭 {texts.COM_SUB}", callback_data=Cd.Admin.com_sub()))
    result.row(InlineKeyboardButton(text=f"🔙 {texts.BACK}", callback_data=Cd.Back.main_menu()))
    return result.as_markup()


def admin_list(ls: list[list[UserDTO]], page_num=0):
    result = InlineKeyboardBuilder()
    len_ls = len(ls)
    count = page_num if len_ls != 1 else 0
    for i in ls[count]:
        result.row(InlineKeyboardButton(text=i.full_name, callback_data='None'))
        result.add(InlineKeyboardButton(text=f"✂️ {texts.DELETE}", callback_data=Cd.Admin.remove_admin(i.user_id)))
    if len(ls) != 1:
        move_back, move_next = get_next_pag(len_ls=len_ls, page_num=page_num)

        callback_data_back = Cd.Admin.move_admins(move_back)
        callback_data_next = Cd.Admin.move_admins(move_next)

        result.row(InlineKeyboardButton(text=f"⬅", callback_data=callback_data_back))
        result.add(InlineKeyboardButton(text=f"{page_num + 1}/{len_ls}", callback_data=f"None"))
        result.add(InlineKeyboardButton(text=f"➡", callback_data=callback_data_next))

    result.row(InlineKeyboardButton(text=f"🔙 {texts.BACK}", callback_data=Cd.Admin.main()))
    return result.as_markup()


def com_chats(ls: list[list[ComSubChatsDTO]], page_num=0):
    result = InlineKeyboardBuilder()
    len_ls = len(ls)
    count = page_num if len_ls != 1 else 0
    for i in ls[count]:
        cb_turn = Cd.Admin.com_chat_toggle_turn(i.chat_id)
        result.row(InlineKeyboardButton(text="🟢" if i.turn else "🔴", callback_data=cb_turn))
        result.add(InlineKeyboardButton(text=i.username, callback_data='None'))
        result.add(InlineKeyboardButton(text=f"✂️ {texts.DELETE}", callback_data=Cd.Admin.remove_com_chat(i.chat_id)))
    if len(ls) != 1:
        move_back, move_next = get_next_pag(len_ls=len_ls, page_num=page_num)

        callback_data_back = Cd.Admin.move_com_chats(move_back)
        callback_data_next = Cd.Admin.move_com_chats(move_next)

        result.row(InlineKeyboardButton(text=f"⬅", callback_data=callback_data_back))
        result.add(InlineKeyboardButton(text=f"{page_num + 1}/{len_ls}", callback_data=f"None"))
        result.add(InlineKeyboardButton(text=f"➡", callback_data=callback_data_next))

    result.row(InlineKeyboardButton(text=f"➕ {texts.ADD}", callback_data=Cd.Admin.add_com_chat()))
    result.add(InlineKeyboardButton(text=f"🔙 {texts.BACK}", callback_data=Cd.Admin.main()))
    return result.as_markup()


def confirm_ross():
    result = InlineKeyboardBuilder()
    confirm = InlineKeyboardButton(text=f"✅ {texts.CONFIRM}", callback_data=Cd.Admin.confirm_ross())
    cancel = InlineKeyboardButton(text=f"❌ {texts.CANCEL}", callback_data=Cd.Admin.main())
    result.row(confirm).add(cancel)
    return result.as_markup()


def back(to, main_menu: bool = False, cancel: bool = False):
    text = f"🔙 {texts.BACK}"
    if cancel is True:
        text = f"❌ {texts.CANCEL}"
    if main_menu is True:
        text = f"🔙 {texts.MAIN_MENU}"
    result = InlineKeyboardBuilder()
    result.add(InlineKeyboardButton(text=text, callback_data=to))
    return result.as_markup()


def subscribe_chats(chat_list: List[ComSubChatsDTO]):
    result = InlineKeyboardBuilder()
    for chat in chat_list:
        link = f"https://t.me/{chat.username}"
        result.row(InlineKeyboardButton(text=chat.username, url=link))
    return result.as_markup()


def add_com_chat(bot_username: str):
    result = InlineKeyboardBuilder()
    url = 'http://t.me/{username}?{command}&admin=change_info+post_messages+edit_messages+delete_messages+restrict_members+invite_users+pin_messages+promote_members+manage_video_chats+anonymous+manage_chat'
    result.row(InlineKeyboardButton(text=f"➕ {texts.ADD_TO_CHANNEL}",
                                    url=url.format(username=bot_username, command='startchannel')))
    result.add(InlineKeyboardButton(text=f"➕ {texts.ADD_TO_GROUP}",
                                    url=url.format(username=bot_username, command='startgroup')))
    result.row(InlineKeyboardButton(text=f"🔙 {texts.BACK}", callback_data=Cd.Admin.com_sub()))
    return result.as_markup()
