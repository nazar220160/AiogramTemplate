from typing import Optional

from src.common.dto import BotChatsCreate, BotChatsUpdate
from src.database.models import BotChats
from src.database.repositories.base import BaseInteractor


class BotChatsWriter(BaseInteractor[BotChats]):

    async def create(self, query: BotChatsCreate) -> Optional[BotChats]:
        return await self.crud.create(**query.model_dump(exclude_none=True))

    async def update(self, chat_id: int, query: BotChatsUpdate) -> Optional[BotChats]:
        result = await self.crud.update(
            self.model.id == chat_id, **query.model_dump(exclude_none=True)
        )
        return result[0] if result else None
