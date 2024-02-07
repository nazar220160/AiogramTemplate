from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot import keyboards
from src.bot.common.filters import IsAdmin
from src.bot.common.middlewares.i18n import gettext as _
from src.bot.routers.admin.router import admin_router
from src.bot.utils.callback import CallbackData as Cb
from src.bot.utils.texts import admin as texts
from src.database.core.gateway import DatabaseGateway


@admin_router.message(Command("admin"), IsAdmin())
async def start(message: types.Message, db: DatabaseGateway):
    all_users = await db.user.reader.select_many()
    await message.answer(
        _(texts.START).format(len_users=len(all_users)), reply_markup=keyboards.admin()
    )


@admin_router.callback_query(lambda c: Cb.extract(c.data).data == Cb.Admin.main())
async def admin_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    db: DatabaseGateway,
) -> None:
    await state.clear()
    await callback.message.delete()
    all_users = await db.user.reader.select_many()
    await callback.message.answer(
        _(texts.START).format(len_users=len(all_users)),
        reply_markup=keyboards.admin(),
    )
