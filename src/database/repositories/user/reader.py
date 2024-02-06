from typing import Any, Optional, Sequence, overload

from sqlalchemy import select

from src.common.types import OrderByType
from src.database.models import User
from src.database.repositories.base import BaseInteractor


class UserReader(BaseInteractor[User]):
    async def select(self, user_id: int) -> Optional[User]:
        return await self.crud.select(self.model.id == user_id)

    @overload
    async def select_many(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: OrderByType,
    ) -> Sequence[User]: ...

    @overload
    async def select_many(
        self,
        *,
        admin: bool,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: OrderByType,
    ) -> Sequence[User]: ...

    @overload
    async def select_many(
        self,
        *,
        blocked: bool,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: OrderByType,
    ) -> Sequence[User]: ...

    async def select_many(
        self,
        *,
        order_by: OrderByType = "ASC",
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs: Any,
    ) -> Sequence[User]:
        if admin := kwargs.get("admin"):
            stmt = (
                select(self.model)
                .where(self.model.admin == admin)
                .offset(offset)
                .limit(limit)
                .order_by(
                    self.model.id.asc() if order_by == "ASC" else self.model.id.desc()
                )
            )
            result = (await self.session.execute(stmt)).scalars().all()
        elif blocked := kwargs.get("blocked"):
            stmt = (
                select(self.model)
                .where(self.model.blocked == blocked)
                .offset(offset)
                .limit(limit)
                .order_by(
                    self.model.id.asc() if order_by == "ASC" else self.model.id.desc()
                )
            )
            result = (await self.session.execute(stmt)).scalars().all()
        else:
            result = await self.crud.select_many(offset=offset, limit=limit)
        return result
    
    
    async def exist(self, user_id: int) -> bool:
        return await self.crud.exists(self.model.id == user_id)
