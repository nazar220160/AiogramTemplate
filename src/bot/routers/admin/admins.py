from aiogram import types
from aiogram.filters import Command

from src.bot import keyboards
from src.bot.common.filters import IsAdmin
from src.bot.common.middlewares.i18n import gettext as _
from src.bot.routers.admin.router import admin_router
from src.bot.utils.callback import CallbackData as Cb
from src.bot.utils.other import paginate
from src.bot.utils.texts import admin as texts
from src.common.dto import (
    UserUpdate,
)
from src.core.config import Config
from src.database.core.gateway import DatabaseGateway


@admin_router.callback_query(lambda c: Cb.extract(c.data).data == Cb.Admin.get_admins())
async def get_admins(callback: types.CallbackQuery, db: DatabaseGateway) -> None:
    list_admins = await db.user.reader.select_many(admin=True)
    pag = paginate(list_items=list_admins, items_per_page=5)
    await callback.message.edit_reply_markup(reply_markup=keyboards.admin_list(ls=pag))


@admin_router.callback_query(
    lambda c: Cb.extract(c.data).data == Cb.Admin.remove_admin()
)
async def remove_admin(
    callback: types.CallbackQuery, db: DatabaseGateway, config: Config
) -> None:
    data = Cb.extract(cd=callback.data)
    if callback.from_user.id not in config.bot.admins:
        await callback.answer(text=_(texts.INSUFFICIENT_PERMISSIONS), show_alert=True)
        return

    await db.user.writer.update(
        user_id=int(data.args[0]), query=UserUpdate(admin=False)
    )
    list_admins = await db.user.reader.select_many(admin=True)

    pag = paginate(list_items=list_admins, items_per_page=5)
    await callback.message.edit_reply_markup(reply_markup=keyboards.admin_list(ls=pag))


@admin_router.callback_query(
    lambda c: Cb.extract(c.data).data == Cb.Admin.move_admins()
)
async def move_admins(callback: types.CallbackQuery, db: DatabaseGateway) -> None:
    data = Cb.extract(cd=callback.data)

    page_num = int(data.args[0])
    list_admins = await db.user.reader.select_many(admin=True)

    pag = paginate(list_items=list_admins, items_per_page=5)
    reply_markup = keyboards.admin_list(pag, page_num=page_num)
    await callback.message.edit_reply_markup(reply_markup=reply_markup)


@admin_router.message(Command("add_admin"), IsAdmin())
async def add_admin(message: types.Message, db: DatabaseGateway):
    message_args = message.text.split()
    if len(message_args) < 2:
        await message.answer(_(texts.FOR_SEND_MESSAGE_ENTER_COMMAND))
        return

    try:
        user_id = int(message_args[1])
        user = await db.user.writer.update(
            user_id=user_id, query=UserUpdate(admin=True)
        )
        if not user:
            await message.answer(_(texts.USER_NOT_FOUND))
            return
        await message.answer(_(texts.SUCCESSFUL))
    except ValueError:
        await message.answer(_(texts.MUST_BE_INTEGER))
