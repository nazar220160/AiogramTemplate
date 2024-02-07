from aiogram import types

from src.bot import keyboards
from src.bot.common.middlewares.i18n import gettext as _
from src.bot.core.models import MyBot
from src.bot.routers.admin.router import admin_router
from src.bot.utils.callback import CallbackData as Cb
from src.bot.utils.other import paginate
from src.bot.utils.texts import admin as texts
from src.common.dto.core import BotChatsUpdate
from src.database.core.gateway import DatabaseGateway


@admin_router.callback_query(lambda c: Cb.extract(c.data).data == Cb.Admin.com_sub())
async def start(callback: types.CallbackQuery, db: DatabaseGateway) -> None:
    await callback.message.delete()
    list_chats = await db.bot_chats.reader.select_many()
    list_chats = [
        i for i in list_chats if i.permissions.get("status") == "administrator"
    ]
    pag = paginate(list_items=list_chats, items_per_page=5)
    await callback.message.answer(
        text=_(texts.ADMIN_PANEL_COM_SUB), reply_markup=keyboards.com_chats(ls=pag)
    )


@admin_router.callback_query(
    lambda c: Cb.extract(c.data).data == Cb.Admin.add_com_chat()
)
async def add_com_chat(callback: types.CallbackQuery, bot: MyBot) -> None:
    await callback.message.delete()
    bot_info = await bot.me()
    reply_markup = keyboards.add_com_chat(bot_username=bot_info.username)
    await callback.message.answer(_(texts.ADD_COM_CHAT), reply_markup=reply_markup)


@admin_router.callback_query(
    lambda c: Cb.extract(c.data).data == Cb.Admin.move_com_chats()
)
async def move_com_chats(callback: types.CallbackQuery, db: DatabaseGateway) -> None:
    data = Cb.extract(callback.data)

    page_num = int(data.args[0])
    list_chats = await db.bot_chats.reader.select_many()
    list_chats = [
        i for i in list_chats if i.permissions.get("status") == "administrator"
    ]

    pag = paginate(list_items=list_chats, items_per_page=5)
    reply_markup = keyboards.com_chats(pag, page_num=page_num)
    await callback.message.edit_reply_markup(reply_markup=reply_markup)


@admin_router.callback_query(
    lambda c: Cb.extract(c.data).data == Cb.Admin.com_chat_toggle_turn()
)
async def com_chat_toggle_turn(
    callback: types.CallbackQuery, db: DatabaseGateway
) -> None:
    data = Cb.extract(callback.data)

    chat_id = int(data.args[0])

    chat_info = await db.bot_chats.reader.select(chat_id=chat_id)
    await db.bot_chats.writer.update(
        chat_id=chat_id, query=BotChatsUpdate(sub=not chat_info.sub)
    )

    list_chats = await db.bot_chats.reader.select_many()
    list_chats = [
        i for i in list_chats if i.permissions.get("status") == "administrator"
    ]

    pag = paginate(list_items=list_chats, items_per_page=5)
    reply_markup = keyboards.com_chats(pag)
    await callback.message.edit_reply_markup(reply_markup=reply_markup)
