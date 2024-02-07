from aiogram import F, types
from aiogram.fsm.context import FSMContext

from src.bot import keyboards
from src.bot.common.filters import IsAdmin
from src.bot.common.middlewares.i18n import gettext as _
from src.bot.common.states.admin import BanUser
from src.bot.routers.admin.router import admin_router
from src.bot.utils.callback import CallbackData as Cb
from src.bot.utils.other import paginate
from src.bot.utils.texts import admin as texts
from src.common.dto import UserUpdate
from src.database.core.gateway import DatabaseGateway


@admin_router.callback_query(
    lambda c: Cb.extract(c.data).data == Cb.Admin.banned_users()
)
async def banned_users(callback: types.CallbackQuery, db: DatabaseGateway) -> None:
    list_banned_users = await db.user.reader.select_many(blocked=True)
    pag = paginate(list_items=list_banned_users, items_per_page=5)
    await callback.message.delete()
    await callback.message.answer(
        text=_(texts.BANNED_USERS), reply_markup=keyboards.banned_users(ls=pag)
    )


@admin_router.callback_query(
    lambda c: Cb.extract(c.data).data == Cb.Admin.move_banned_users()
)
async def move_banned_users(callback: types.CallbackQuery, db: DatabaseGateway) -> None:
    data = Cb.extract(cd=callback.data)
    page_num = int(data.args[0])
    list_banned_users = await db.user.reader.select_many(blocked=True)
    pag = paginate(list_items=list_banned_users, items_per_page=5)
    reply_markup = keyboards.banned_users(ls=pag, page_num=page_num)
    await callback.message.edit_reply_markup(reply_markup=reply_markup)


@admin_router.callback_query(lambda c: Cb.extract(c.data).data == Cb.Admin.unban())
async def unban_user(callback: types.CallbackQuery, db: DatabaseGateway) -> None:
    data = Cb.extract(cd=callback.data)

    user_id = int(data.args[0])

    await db.user.writer.update(user_id=user_id, query=UserUpdate(blocked=False))

    list_banned_users = await db.user.reader.select_many(blocked=True)
    pag = paginate(list_items=list_banned_users, items_per_page=5)
    reply_markup = keyboards.banned_users(ls=pag)
    await callback.message.edit_reply_markup(reply_markup=reply_markup)
    await callback.answer(text=_(texts.SUCCESSFUL))


@admin_router.callback_query(lambda c: Cb.extract(c.data).data == Cb.Admin.ban())
async def ban_user(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.message.delete()
    await callback.message.answer(
        text=_(texts.SEND_USER_ID_TO_BAN),
        reply_markup=keyboards.back(to=Cb.Admin.main(), cancel=True),
    )
    await state.set_state(BanUser.user_id)


@admin_router.message(F.text, BanUser.user_id, IsAdmin())
async def get_user_id_ban_user(
    message: types.Message, db: DatabaseGateway, state: FSMContext
):
    try:
        user_id = int(message.text)
    except ValueError:
        await message.reply(_(texts.MUST_BE_INTEGER))
        return
    check_user = await db.user.reader.select(user_id=user_id)
    if not check_user:
        await message.reply(
            _(texts.USER_NOT_FOUND),
            reply_markup=keyboards.back(to=Cb.Admin.main(), cancel=True),
        )
        return

    await db.user.writer.update(user_id=user_id, query=UserUpdate(blocked=True))
    await message.reply(
        text=_(texts.BAN_USER_SUCCESSFUL).format(check_user.first_name),
        reply_markup=keyboards.back(to=Cb.Admin.main(), main_menu=True),
    )
    await state.clear()
