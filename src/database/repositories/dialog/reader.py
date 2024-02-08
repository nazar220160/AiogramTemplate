from typing import Any, Optional, Sequence, overload

from sqlalchemy import select

from src.common.types import OrderByType
from src.database.exceptions import InvalidParamsError
from src.database.models import Dialog
from src.database.repositories.base import BaseInteractor


class DialogReader(BaseInteractor[Dialog]):

    @overload
    async def select(self, *, dialog_id: int) -> Optional[Dialog]: ...

    @overload
    async def select(self, *, chat_id: int) -> Optional[Dialog]: ...

    async def select(self, **kwargs: Any) -> Optional[Dialog]:
        if dialog_id := kwargs.get("dialog_id"):
            result = await self.crud.select(self.model.id == dialog_id)
        elif chat_id := kwargs.get("chat_id"):
            result = await self.crud.select(self.model.chat_id == chat_id)
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
    ) -> Sequence[Dialog]: ...

    @overload
    async def select_many(
        self,
        *,
        session_id: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: OrderByType,
    ) -> Sequence[Dialog]: ...

    @overload
    async def select_many(
        self,
        *,
        session_id: int,
        chat_type: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: OrderByType,
    ) -> Sequence[Dialog]: ...

    @overload
    async def select_many(
        self,
        *,
        user_id: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: OrderByType,
    ) -> Sequence[Dialog]: ...

    async def select_many(
        self,
        *,
        order_by: OrderByType = "ASC",
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs: Any,
    ) -> Sequence[Dialog]:
        if session_id := kwargs.get("session_id"):
            if chat_type := kwargs.get("chat_type"):
                stmt = (
                    select(self.model)
                    .where(
                        self.model.session_id == session_id,
                        self.model.chat_type == chat_type,
                    )
                    .offset(offset)
                    .limit(limit)
                    .order_by(
                        self.model.id.asc()
                        if order_by == "ASC"
                        else self.model.id.desc()
                    )
                )
                result = (await self.session.execute(stmt)).scalars().all()
            else:
                stmt = (
                    select(self.model)
                    .where(self.model.session_id == session_id)
                    .offset(offset)
                    .limit(limit)
                    .order_by(
                        self.model.id.asc()
                        if order_by == "ASC"
                        else self.model.id.desc()
                    )
                )
            result = (await self.session.execute(stmt)).scalars().all()
        elif user_id := kwargs.get("user_id"):
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
        else:
            result = await self.crud.select_many(offset=offset, limit=limit)
        return result

    async def exist(self, dialog_id: int) -> bool:
        return await self.crud.exists(self.model.id == dialog_id)
