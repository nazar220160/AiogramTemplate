from typing import Any, Optional, Sequence, overload

from sqlalchemy import select

from src.common.types import OrderByType
from src.database.exceptions import InvalidParamsError
from src.database.models import Session
from src.database.repositories.base import BaseInteractor


class SessionReader(BaseInteractor[Session]):

    @overload
    async def select(self, *, session_id: int) -> Optional[Session]: ...

    @overload
    async def select(self, *, session: str) -> Optional[Session]: ...

    async def select(self, **kwargs: Any) -> Optional[Session]:
        if session_id := kwargs.get("session_id"):
            result = await self.crud.select(self.model.id == session_id)
        elif session := kwargs.get("session"):
            result = await self.crud.select(self.model.session == session)
        else:
            raise InvalidParamsError(f"{tuple(kwargs.keys())} is not valid params")
        return result

    @overload
    async def select_many(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: OrderByType,
    ) -> Sequence[Session]: ...

    @overload
    async def select_many(
        self,
        *,
        user_id: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: OrderByType,
    ) -> Sequence[Session]: ...

    @overload
    async def select_many(
        self,
        *,
        phone_number: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: OrderByType,
    ) -> Sequence[Session]: ...

    async def select_many(
        self,
        *,
        order_by: OrderByType = "ASC",
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs: Any,
    ) -> Sequence[Session]:
        if user_id := kwargs.get("user_id"):
            stmt = (
                select(self.model)
                .where(self.model.user_id == user_id)
                .offset(offset)
                .limit(limit)
                .order_by(
                    self.model.id.asc() if order_by == "ASC" else self.model.id.desc()
                )
            )
            result = (await self.session.execute(stmt)).scalars().all()
        elif phone_number := kwargs.get("phone_number"):
            stmt = (
                select(self.model)
                .where(self.model.phone_number == phone_number)
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
