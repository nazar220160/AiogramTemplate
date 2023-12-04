from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    TypeAlias,
    Union,
)

from aiogram import types

BackButtonReturnType: TypeAlias = Callable[..., Coroutine[Any, Any, Any]]


class ChatMessagePagination:

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


class ChatFunctionPagination:

    def __init__(self) -> None:
        self.users: Dict[Union[int, str], Any] = {}

    def get_last_message(
            self,
            user_id: int,
    ) -> Optional[BackButtonReturnType]:
        last_message_func_stack: List[BackButtonReturnType]
        last_message_func_stack = self.users.get(user_id, [])

        if len(last_message_func_stack) <= 1:
            return None

        last_message_func_stack.pop()
        return last_message_func_stack[-1]

    def set_message(
            self,
            user_id: int,
            func: BackButtonReturnType,
            start_message: bool = False,
    ) -> None:
        stack = self.users.get(user_id, [])
        stack.append(func)
        self.users[user_id] = stack if not start_message else [func]
