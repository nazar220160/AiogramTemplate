from __future__ import annotations

import importlib
from datetime import datetime
from typing import List, Optional

from src.common.dto.base import DTO
from src.utils.enums import Status

__all__ = [
    "BotChatsCreate",
    "BotChatsUpdate",
    "BotChats",
    "QuestionUpdate",
    "QuestionCreate",
    "Question",
    "UserCreate",
    "UserUpdate",
    "User",
]


def rebuild_all_models_in_current_module() -> None:
    module = importlib.import_module(__name__)
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, type) and issubclass(attr, DTO) and attr != DTO:
            attr.model_rebuild()


class BotChats(DTO):
    chat_id: int
    username: Optional[str] = None
    title: str

    permissions: dict
    sub: bool

    created_at: datetime
    updated_at: datetime
    deleted_at: datetime


class BotChatsCreate(DTO):
    id: int
    username: Optional[str] = None
    title: str

    permissions: dict
    sub: Optional[bool] = False


class BotChatsUpdate(DTO):
    chat_id: Optional[int] = None
    username: Optional[str] = None
    title: Optional[str] = None

    permissions: Optional[dict] = None
    sub: Optional[bool] = None


class Question(DTO):
    id: int
    user_message_id: int
    admin_message_id: int
    status: Optional[Status]
    user_id: int
    user: Optional["User"]

    created_at: datetime
    updated_at: datetime
    deleted_at: datetime


class QuestionCreate(DTO):
    user_message_id: int
    admin_message_id: int
    status: Optional[Status] = Status.PENDING
    user_id: int


class QuestionUpdate(DTO):
    user_message_id: Optional[int] = None
    admin_message_id: Optional[int] = None
    status: Optional[Status] = None
    user_id: Optional[int] = None


class User(DTO):
    id: int
    first_name: str
    username: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    blocked: bool
    admin: bool

    questions: List["Question"]

    created_at: datetime
    updated_at: datetime
    deleted_at: datetime


class UserCreate(DTO):
    id: int
    first_name: str
    username: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    blocked: Optional[bool] = False
    admin: Optional[bool] = False


class UserUpdate(DTO):
    first_name: Optional[bool] = None
    username: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    blocked: Optional[bool] = None
    admin: Optional[bool] = None
