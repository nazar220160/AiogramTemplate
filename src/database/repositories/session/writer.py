from typing import Optional

from src.common.dto import SessionCreate, SessionUpdate
from src.database.models import Session
from src.database.repositories.base import BaseInteractor


class SessionWriter(BaseInteractor[Session]):

    async def create(self, query: SessionCreate) -> Optional[Session]:
        return await self.crud.create(**query.model_dump(exclude_none=True))

    async def update(self, session_id: int, query: SessionUpdate) -> Optional[Session]:
        result = await self.crud.update(
            self.model.id == session_id, **query.model_dump(exclude_none=True)
        )
        return result[0] if result else None
