from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

from src.database.core.unit_of_work import SQLAlchemyUnitOfWork
from src.database.repositories import (
    BotChatsRepository,
    DialogRepository,
    QuestionRepository,
    SessionRepository,
    UserRepository,
)


class DatabaseGateway:
    __slots__ = ("uow",)

    def __init__(self, unit_of_work: SQLAlchemyUnitOfWork) -> None:
        self.uow = unit_of_work

    async def __aenter__(self) -> DatabaseGateway:
        await self.uow.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.uow.__aexit__(exc_type, exc_value, traceback)

    @property
    def user(self) -> UserRepository:
        return UserRepository(self.uow.session)

    @property
    def question(self) -> QuestionRepository:
        return QuestionRepository(self.uow.session)

    @property
    def bot_chats(self) -> BotChatsRepository:
        return BotChatsRepository(self.uow.session)

    @property
    def session(self) -> SessionRepository:
        return SessionRepository(self.uow.session)
    
    @property
    def dialog(self) -> DialogRepository:
        return DialogRepository(self.uow.session)


def database_gateway_factory(unit_of_work: SQLAlchemyUnitOfWork) -> DatabaseGateway:
    return DatabaseGateway(unit_of_work)
