import random

from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from src.bot import keyboards
from src.config.settings import Settings
from src.bot.utils.texts import client as texts
from src.database.core import Database
from src.common.dto import QuestionCreate
from src.bot.common.states.main import Support

from src.bot.utils.callback import CallbackData as Cb
from src.bot.routers.client.router import client_router
from src.bot.common.middlewares.i18n import gettext as _


@client_router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=_(texts.START), reply_markup=keyboards.start())


@client_router.message(Command('support'))
async def support(message: types.Message, state: FSMContext):
    await state.set_state(Support.message)
    await message.reply(text=_(texts.SUPPORT),
                        reply_markup=keyboards.back(
                            to=Cb.Back.main_menu(),
                            main_menu=True
                        ))


@client_router.message(Support.message)
async def get_support_message(message: types.Message, state: FSMContext,
                              settings: Settings, db: Database):
    await state.clear()

    db_admins = [user.user_id for user in await db.user.get_admins()]
    admins = db_admins + settings.admins

    if not admins:
        await message.reply(_(texts.ADMINS_NOT_FOUND))
        return

    mes = await message.forward(chat_id=random.choice(admins))
    await db.question.create(query=QuestionCreate(
        user_id=message.from_user.id,
        user_message_id=message.message_id,
        admin_message_id=mes.message_id
    ))
    await message.reply(_(texts.SUPPORT_YOUR_MESSAGE_SEND_ADMIN))


@client_router.callback_query(lambda c: Cb.extract(c.data, True).data == Cb.Back())
async def back(callback: types.CallbackQuery, state: FSMContext):
    data = Cb.extract(callback.data)
    if data.data == Cb.Back.main_menu():
        await state.clear()
        await callback.message.delete()

        reply_markup = keyboards.start()

        await callback.message.answer(_(texts.START), reply_markup=reply_markup)
