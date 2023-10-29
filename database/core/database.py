from __future__ import annotations

from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession

from database.core.unit_of_work import UnitOfWork
from database.core.connection import async_session
from database.core.mediator import build_mediator
from database.repositories import (
    UserRepository,
    QuestionRepository,
    ComSubChatsRepository,
)


class Database:

    def __init__(self, db_url: str, session: Optional[AsyncSession] = None) -> None:
        if session is None:
            session = async_session(db_url=db_url)
        self._uow = UnitOfWork(session)
        self._mediator = build_mediator(session)

    async def __aenter__(self) -> Database:
        await self._uow.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._uow.__aexit__(*args)
        return None

    @property
    def user(self) -> UserRepository:
        return self._mediator.userrepository  # type: ignore

    @property
    def question(self) -> QuestionRepository:
        return self._mediator.questionrepository  # type: ignore

    @property
    def com_sub_chats(self) -> ComSubChatsRepository:
        return self._mediator.comsubchatsrepository  # type: ignore
