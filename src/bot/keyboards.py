from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from src.bot.common.middlewares.i18n import gettext as _
from src.bot.utils.callback import CallbackData as Cd
from src.bot.utils.other import get_next_pag
from src.bot.utils.texts import buttons as texts
from src.database.models import BotChats, User
from src.database.models.dialog import Dialog
from src.database.models.session import Session


def start():
    result = InlineKeyboardBuilder()
    result.row(
        InlineKeyboardButton(
            text=f"👤 {_(texts.ACCOUNTS)}", callback_data=Cd.Start.accounts()
        )
    )
    return result.as_markup()


def admin():
    result = InlineKeyboardBuilder()
    result.row(
        InlineKeyboardButton(
            text=f"📢 {_(texts.NEWSLETTER)}", callback_data=Cd.Admin.ross()
        )
    )
    result.add(
        InlineKeyboardButton(
            text=f"👥 {_(texts.ADMINS)}", callback_data=Cd.Admin.get_admins()
        )
    )
    result.row(
        InlineKeyboardButton(
            text=f"💭 {_(texts.COM_SUB)}", callback_data=Cd.Admin.com_sub()
        )
    )
    result.row(
        InlineKeyboardButton(
            text=f"🚫 {_(texts.BANNED_USERS)}", callback_data=Cd.Admin.banned_users()
        )
    )
    result.row(
        InlineKeyboardButton(
            text=f"🔙 {_(texts.BACK)}", callback_data=Cd.Back.main_menu()
        )
    )
    return result.as_markup()


def admin_list(ls: list[list[User]], page_num=0):
    result = InlineKeyboardBuilder()
    len_ls = len(ls)
    count = page_num if len_ls != 1 else 0
    for i in ls[count]:
        result.row(InlineKeyboardButton(text=i.first_name, callback_data="None"))
        result.add(
            InlineKeyboardButton(
                text=f"✂️ {_(texts.DELETE)}",
                callback_data=Cd.Admin.remove_admin(i.id),
            )
        )
    if len(ls) != 1:
        move_back, move_next = get_next_pag(len_ls=len_ls, page_num=page_num)

        callback_data_back = Cd.Admin.move_admins(move_back)
        callback_data_next = Cd.Admin.move_admins(move_next)

        result.row(InlineKeyboardButton(text="⬅", callback_data=callback_data_back))
        result.add(
            InlineKeyboardButton(text=f"{page_num + 1}/{len_ls}", callback_data="None")
        )
        result.add(InlineKeyboardButton(text="➡", callback_data=callback_data_next))

    result.row(
        InlineKeyboardButton(text=f"🔙 {_(texts.BACK)}", callback_data=Cd.Admin.main())
    )
    return result.as_markup()


def com_chats(ls: list[list[BotChats]], page_num=0):
    result = InlineKeyboardBuilder()
    len_ls = len(ls)
    count = page_num if len_ls != 1 else 0
    for i in ls[count]:
        cb_turn = Cd.Admin.com_chat_toggle_turn(i.id)
        result.row(
            InlineKeyboardButton(text="🟢" if i.sub else "🔴", callback_data=cb_turn)
        )
        result.add(InlineKeyboardButton(text=i.username, callback_data="None"))
        result.add(
            InlineKeyboardButton(text="🟢" if i.sub else "🔴", callback_data=cb_turn)
        )
    if len(ls) != 1:
        move_back, move_next = get_next_pag(len_ls=len_ls, page_num=page_num)

        callback_data_back = Cd.Admin.move_com_chats(move_back)
        callback_data_next = Cd.Admin.move_com_chats(move_next)

        result.row(InlineKeyboardButton(text="⬅", callback_data=callback_data_back))
        result.add(
            InlineKeyboardButton(text=f"{page_num + 1}/{len_ls}", callback_data="None")
        )
        result.add(InlineKeyboardButton(text="➡", callback_data=callback_data_next))

    result.row(
        InlineKeyboardButton(
            text=f"➕ {_(texts.ADD)}", callback_data=Cd.Admin.add_com_chat()
        )
    )
    result.add(
        InlineKeyboardButton(text=f"🔙 {_(texts.BACK)}", callback_data=Cd.Admin.main())
    )
    return result.as_markup()


def confirm_ross():
    result = InlineKeyboardBuilder()
    confirm = InlineKeyboardButton(
        text=f"✅ {_(texts.CONFIRM)}", callback_data=Cd.Admin.confirm_ross()
    )
    cancel = InlineKeyboardButton(
        text=f"❌ {_(texts.CANCEL)}", callback_data=Cd.Admin.main()
    )
    result.row(confirm).add(cancel)
    return result.as_markup()


def back(to, main_menu: bool = False, cancel: bool = False):
    text = f"🔙 {_(texts.BACK)}"
    if cancel is True:
        text = f"❌ {_(texts.CANCEL)}"
    if main_menu is True:
        text = f"🔙 {_(texts.MAIN_MENU)}"
    result = InlineKeyboardBuilder()
    result.add(InlineKeyboardButton(text=text, callback_data=to))
    return result.as_markup()


def subscribe_chats(chat_list: List[BotChats]):
    result = InlineKeyboardBuilder()
    for chat in chat_list:
        link = f"https://t.me/{chat.username}"
        result.row(InlineKeyboardButton(text=chat.username, url=link))
    return result.as_markup()


def add_com_chat(bot_username: str):
    result = InlineKeyboardBuilder()
    url = "http://t.me/{username}?{command}&admin=change_info+post_messages+edit_messages+delete_messages+restrict_members+invite_users+pin_messages+promote_members+manage_video_chats+anonymous+manage_chat"
    result.row(
        InlineKeyboardButton(
            text=f"➕ {_(texts.ADD_TO_CHANNEL)}",
            url=url.format(username=bot_username, command="startchannel"),
        )
    )
    result.add(
        InlineKeyboardButton(
            text=f"➕ {_(texts.ADD_TO_GROUP)}",
            url=url.format(username=bot_username, command="startgroup"),
        )
    )
    result.row(
        InlineKeyboardButton(
            text=f"🔙 {_(texts.BACK)}", callback_data=Cd.Admin.com_sub()
        )
    )
    return result.as_markup()


def banned_users(ls: list[list[User]], page_num=0):
    result = InlineKeyboardBuilder()
    len_ls = len(ls)
    count = page_num if len_ls != 1 else 0
    for i in ls[count]:
        result.row(InlineKeyboardButton(text=i.first_name, callback_data="None"))
        result.add(
            InlineKeyboardButton(
                text=f"✂️ {_(texts.UNBAN)}", callback_data=Cd.Admin.unban(i.id)
            )
        )
    if len(ls) != 1:
        move_back, move_next = get_next_pag(len_ls=len_ls, page_num=page_num)

        callback_data_back = Cd.Admin.move_banned_users(move_back)
        callback_data_next = Cd.Admin.move_banned_users(move_next)

        result.row(InlineKeyboardButton(text="⬅", callback_data=callback_data_back))
        result.add(
            InlineKeyboardButton(text=f"{page_num + 1}/{len_ls}", callback_data="None")
        )
        result.add(InlineKeyboardButton(text="➡", callback_data=callback_data_next))

    result.row(
        InlineKeyboardButton(text=f"➕ {_(texts.ADD)}", callback_data=Cd.Admin.ban())
    )
    result.add(
        InlineKeyboardButton(text=f"🔙 {_(texts.BACK)}", callback_data=Cd.Admin.main())
    )
    return result.as_markup()


def accounts_list(
    ls: List[List[Session]], page_num=0, data="account", settings: bool = True
):
    result = InlineKeyboardBuilder()
    len_ls = len(ls)
    count = page_num if len_ls != 1 else 0
    for i in ls[count]:
        text = f"{i.phone_number}: {i.first_name} {i.last_name if i.last_name else ''}"
        result.row(
            InlineKeyboardButton(
                text=text, callback_data=Cd.Accounts.select(i.id, data)
            )
        )
        if settings is True:
            result.add(
                InlineKeyboardButton(
                    text=f"⚙️ {_(texts.SETTINGS)}",
                    callback_data=Cd.Accounts.settings(i.id),
                )
            )
    if len_ls != 1:
        move_back, move_next = get_next_pag(len_ls=len_ls, page_num=page_num)
        result.row(
            InlineKeyboardButton(
                text="⬅", callback_data=Cd.Accounts.move(move_back, settings, data)
            )
        )
        result.add(
            InlineKeyboardButton(text=f"{page_num + 1}/{len_ls}", callback_data="None")
        )
        result.add(
            InlineKeyboardButton(
                text="➡", callback_data=Cd.Accounts.move(move_next, settings, data)
            )
        )

    result.row(
        InlineKeyboardButton(text=f"➕ {_(texts.ADD)}", callback_data=Cd.Accounts.add())
    )
    result.add(
        InlineKeyboardButton(
            text=f"🔙 {_(texts.MAIN_MENU)}", callback_data=Cd.Back.main_menu()
        )
    )
    return result.as_markup()


def auth_account(test_net: bool = False):
    result = InlineKeyboardBuilder()
    result.row(
        InlineKeyboardButton(
            text=f"{'🧪' if test_net else '🏘'} {_(texts.NETWORK)}",
            callback_data=Cd.Accounts.switch_network(int(test_net)),
        )
    )
    result.row(
        InlineKeyboardButton(
            text=f"❌ {_(texts.CANCEL)}", callback_data=Cd.Start.accounts()
        )
    )

    result.add(
        InlineKeyboardButton(
            text=f"📸 {_(texts.AUTH_WITH_QR)}", callback_data=Cd.Accounts.auth_with_qr()
        )
    )
    return result.as_markup()


def session_settings(included: bool, session_id: int):
    result = InlineKeyboardBuilder()
    text_turn = f"✅ {_(texts.TURN_OFF)}" if included else f"❌ {_(texts.TURN_ON)}"
    result.add(
        InlineKeyboardButton(
            text=text_turn, callback_data=Cd.AccountSettings.turn(session_id)
        )
    )
    result.add(
        InlineKeyboardButton(
            text=f"🗑 {_(texts.DELETE)}",
            callback_data=Cd.AccountSettings.remove(session_id),
        )
    )
    result.row(InlineKeyboardButton(text=f"📋 {_(texts.CHATS_LIST)}", callback_data=Cd.AccountSettings.dialogs(session_id)))

    result.add(
        InlineKeyboardButton(
            text=f"🔙 {_(texts.BACK)}", callback_data=Cd.Start.accounts()
        )
    )
    return result.as_markup()


def dialogs(ls: List[List[Dialog]], account_id: int, page_num=0, data: str = ""):
    result = InlineKeyboardBuilder()
    len_ls = len(ls)
    count = page_num if len_ls != 1 else 0
    for i in ls[count]:
        text_button = f"{i.chat_title} ({i.chat_id})"
        result.row(
            InlineKeyboardButton(
                text=text_button,
                callback_data=Cd.Dialogs.select(i.chat_id, account_id, data),
            )
        )
    if len_ls != 1:
        move_back, move_next = get_next_pag(len_ls=len_ls, page_num=page_num)
        result.row(
            InlineKeyboardButton(
                text="⬅", callback_data=Cd.Dialogs.move(move_back, account_id, data)
            )
        )
        result.add(
            InlineKeyboardButton(text=f"{page_num + 1}/{len_ls}", callback_data="None")
        )
        result.add(
            InlineKeyboardButton(
                text="➡", callback_data=Cd.Dialogs.move(move_next, account_id, data)
            )
        )

    update_list_cb = Cd.Dialogs.update(page_num, account_id, data)
    result.row(
        InlineKeyboardButton(
            text=f"🔄 {_(texts.UPDATE_LIST)}", callback_data=update_list_cb
        )
    )
    result.add(
        InlineKeyboardButton(
            text=f"🔙 {_(texts.MAIN_MENU)}", callback_data=Cd.Back.main_menu()
        )
    )

    return result.as_markup()
