from aiogram.fsm.state import StatesGroup, State


class Newsletter(StatesGroup):
    message = State()


class BanUser(StatesGroup):
    user_id = State()
