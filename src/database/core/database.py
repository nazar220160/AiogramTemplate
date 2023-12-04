from __future__ import annotations

from typing import Optional, Any, cast

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core.unit_of_work import UnitOfWork
from src.database.core.connection import async_session
from src.database.core.mediator import build_mediator
from src.database.repositories import (
    UserRepository,
    QuestionRepository,
    ComSubChatsRepository,
)


class Database:

    def __init__(self, db_url: str, session: Optional[AsyncSession] = None) -> None:
        if session is None:
            session = async_session(db_url=db_url)

        self._session = session
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
        return cast(UserRepository, self._mediator.userrepository)

    @property
    def question(self) -> QuestionRepository:
        return cast(QuestionRepository, self._mediator.questionrepository)

    @property
    def com_sub_chats(self) -> ComSubChatsRepository:
        return cast(ComSubChatsRepository, self._mediator.comsubchatsrepository)
