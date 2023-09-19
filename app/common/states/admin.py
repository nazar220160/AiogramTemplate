from aiogram.fsm.state import StatesGroup, State


class Newsletter(StatesGroup):
    message = State()
