from typing import (
    Optional,
    Type,
    List,
)

from src.database.converters import convert_com_sub_chats_model_to_dto
from src.common.dto import (
    ComSubChatsCreate,
    ComSubChatsDTO,
    ComSubChatsUpdate,
)
from src.database.interfaces.repositories.base import Repository
from src.database.models import ComSubChats
from src.database.repositories.base import BaseRepository


class ComSubChatsRepository(
    BaseRepository[ComSubChats],
    Repository[int, ComSubChatsDTO, ComSubChatsCreate, ComSubChatsUpdate]
):
    model: Type[ComSubChats] = ComSubChats

    async def create(self, query: ComSubChatsCreate) -> Optional[ComSubChatsDTO]:
        result = await self._crud.create(**query.model_dump(exclude_none=True))
        if not result:
            return None

        return convert_com_sub_chats_model_to_dto(result)

    async def select(self, chat_id: int) -> Optional[ComSubChatsDTO]:
        result = await self._crud.select(self.model.chat_id == chat_id)
        if not result:
            return None

        return convert_com_sub_chats_model_to_dto(result)

    async def select_many(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> List[ComSubChatsDTO]:
        result = await self._crud.select_many(offset=offset, limit=limit)
        return [convert_com_sub_chats_model_to_dto(model) for model in result]

    async def get_chats_turn_on(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = None
    ) -> List[ComSubChatsDTO]:
        result = await self._crud.select_many(self.model.turn, offset=offset, limit=limit)
        return [convert_com_sub_chats_model_to_dto(model) for model in result]

    async def update(
            self, chat_id: int, query: ComSubChatsUpdate, exclude_none: bool = True
    ) -> List[ComSubChatsDTO]:
        result = await self._crud.update(
            self.model.chat_id == chat_id,
            **query.model_dump(exclude_none=exclude_none)
        )
        return [convert_com_sub_chats_model_to_dto(model) for model in result]

    async def delete(self, chat_id: int) -> List[ComSubChatsDTO]:
        result = await self._crud.delete(self.model.chat_id == chat_id)
        return [convert_com_sub_chats_model_to_dto(model) for model in result]
