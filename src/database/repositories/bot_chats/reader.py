from typing import Any, Optional, Sequence, overload

from sqlalchemy import select

from src.database.models import BotChats
from src.database.repositories.base import BaseInteractor


class BotChatsReader(BaseInteractor[BotChats]):

    async def select(self, chat_id: int) -> Optional[BotChats]:
        result = await self.crud.select(self.model.id == chat_id)
        return result

    @overload
    async def select_many(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Sequence[BotChats]: ...

    @overload
    async def select_many(
        self,
        *,
        sub: bool,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Sequence[BotChats]: ...

    async def select_many(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs: Any,
    ) -> Sequence[BotChats]:
        if sub := kwargs.get("sub"):
            stmt = (
                select(self.model)
                .where(self.model.sub == sub)
                .offset(offset)
                .limit(limit)
            )
            result = (await self.session.execute(stmt)).scalars().all()
        else:
            result = await self.crud.select_many(offset=offset, limit=limit)
        return result
    
    
    async def exist(self, chat_id: int) -> bool:
        result = await self.crud.exists(self.model.id == chat_id)
        return result
