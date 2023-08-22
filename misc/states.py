from aiogram.fsm.state import StatesGroup, State


class Admin(StatesGroup):
    ross = State()


class Support(StatesGroup):
    message = State()
