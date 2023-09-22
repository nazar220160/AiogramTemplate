from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.core.settings import Settings
from app.utils import texts
from app import keyboards
from app.database.core import Database
from app.database.dto import UserCreate, QuestionCreate
from app.common.states.main import Support

from app.utils.callback import CallbackData as Cb
from app.routers.client.router import client_router


@client_router.message(CommandStart())
async def start(message: types.Message, state: FSMContext, db: Database):
    user_info = await db.user.select(user_id=message.from_user.id)
    if not user_info:
        await db.user.create(query=UserCreate(
            user_id=message.from_user.id,
            **message.from_user.model_dump(exclude_none=False, exclude='id')
        ))
    await state.clear()

    reply_markup = keyboards.inline.start()
    await message.answer(text=texts.main.START,
                         reply_markup=reply_markup)


@client_router.message(Command('support'))
async def support(message: types.Message, state: FSMContext):
    await state.set_state(Support.message)
    await message.reply(text=texts.main.SUPPORT, reply_markup=keyboards.inline.support())


@client_router.message(Support.message)
async def get_support_message(message: types.Message, state: FSMContext,
                              settings: Settings, db: Database):
    await state.clear()
    mes = await message.forward(chat_id=settings.admins[0])
    await db.question.create(query=QuestionCreate(
        user_message_id=message.message_id,
        admin_message_id=mes.message_id
    ))
    await message.reply("Ваше сообщение отправлено администратору. Ожидайте ответа.")


@client_router.callback_query(lambda c: Cb.extract(c.data, True).data == Cb.Back())
async def back(callback: types.CallbackQuery, state: FSMContext):
    data = Cb.extract(callback.data)
    if data.data == Cb.Back.main_manu():
        await state.clear()
        await callback.message.delete()

        reply_markup = keyboards.inline.start()

        await callback.message.answer(texts.main.START,
                                      reply_markup=reply_markup)
