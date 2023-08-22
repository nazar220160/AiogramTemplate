from aiogram import Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
import texts.main


async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=texts.main.start())


def register_main_handlers(dp: Dispatcher):
    dp.message.register(start, CommandStart())
