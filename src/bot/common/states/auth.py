from aiogram.fsm.state import StatesGroup, State


class SessionCreation(StatesGroup):
    phone_number = State()
    code = State()
    password = State()
