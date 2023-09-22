from typing import (
    Dict,
    Any,
    Optional,
    List,
)

from aiogram import types


class Chat:

    def __init__(self) -> None:
        self.users: Dict[int, Any] = {}

    def get_last_message(
            self,
            user_id: int,
            default_message: Optional[types.Message] = None
    ) -> types.Message:
        last_message: List[types.Message]
        last_message = self.users.get(user_id, [])

        if len(last_message) <= 1:
            return default_message or last_message[-1]

        last_message.pop()
        return last_message[-1]

    def set_message(
            self,
            user_id: int,
            message: types.Message,
            start_message: bool = False,
    ) -> None:
        stack = self.users.get(user_id, [])
        stack.append(message)
        self.users[user_id] = stack if not start_message else [message]
