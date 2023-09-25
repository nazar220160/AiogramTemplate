from aiogram.fsm.state import StatesGroup, State


class Newsletter(StatesGroup):
    message = State()


class ComChatCreator(StatesGroup):
    chat_id = State()
