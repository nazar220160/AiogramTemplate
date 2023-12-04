from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    Final,
    List,
    Optional,
    Sequence,
    Union,
)

DEFAULT_PAGINATION_LIMIT: Final[int] = 10


class InMemoryDataPagination:

    def __init__(self, data: List[Any], text: str, func: Callable[..., Any]) -> None:
        self.data = data
        self.text = text
        self.func = func
        self._page = 0
        self._limit = DEFAULT_PAGINATION_LIMIT

    def is_next_data_exists(self) -> bool:

        end = self._page + 10
        next_data = self.data[self._page:end]

        if not next_data:
            return False

        return True

    def is_previous_data_exists(self) -> bool:

        start = self._page - 20 if (self._page - 20) > 0 else 0
        end = self._page - 10
        previous_data = self.data[start:end]

        if not previous_data:
            return False

        return True

    def next(self) -> List[Any]:

        end = self._page + 10
        next_data = self.data[self._page:end]

        if not next_data:
            return []

        self._page = end

        return next_data

    def previous(self) -> List[Any]:

        start = self._page - 20 if (self._page - 20) > 0 else 0
        end = self._page - 10
        previous_data = self.data[start:end]

        if not previous_data:
            return []

        self._page = end
        return previous_data


class DataPaginationMediator:

    def __init__(self) -> None:
        self.data: Dict[int, InMemoryDataPagination] = {}

    def add(self, user_id: int, data: List[Any], text: str, func: Callable[..., Any]) -> None:
        self.data[user_id] = InMemoryDataPagination(data, text, func)

    def get(self, user_id: int) -> Optional[InMemoryDataPagination]:
        return self.data.get(user_id)

    def clear(self, user_id: int) -> None:
        self.data.pop(user_id, None)


class AsyncDatabaseOffsetPagination:

    def __init__(
            self,
            dfunc: Callable[..., Any],
            func: Callable[..., Coroutine[Any, Any, Sequence[Any]]],
            text: str,
            page: int = 0,
            **kwargs: Any,
    ) -> None:

        self.text = text
        self.dfunc = dfunc
        self.func = func
        self.kwargs = kwargs
        self._page = page
        self._limit = DEFAULT_PAGINATION_LIMIT
        if 'offset' not in self.kwargs:
            self.kwargs['offset'] = self._page
        if 'limit' not in self.kwargs:
            self.kwargs['limit'] = self._limit

    @property
    def current_page(self) -> int:
        return self._page

    @current_page.setter
    def current_page(self, value: int) -> None:
        self._page = value

    async def is_next_data_exists(self) -> bool:
        next_page_offset = self._page * self._limit
        self.kwargs['offset'] = next_page_offset
        exists = await self.func(**self.kwargs)
        self.kwargs['offset'] = (self._page - 1) * self._limit
        return bool(exists)

    async def is_previous_data_exists(self) -> bool:
        return self._page > 1

    async def next(self) -> Union[Sequence[Any], List[Any]]:

        self._page += 1
        self.kwargs['offset'] = (self._page - 1) * self._limit
        return await self.func(**self.kwargs)

    async def previous(self) -> Union[Sequence[Any], List[Any]]:
        if self._page > 1:
            self._page -= 1
            self.kwargs['offset'] = (self._page - 1) * self._limit
            return await self.func(**self.kwargs)
        return []


class DatabaseDataPaginationMediator:

    def __init__(self) -> None:
        self.data: Dict[int, AsyncDatabaseOffsetPagination] = {}

    def add(
            self,
            user_id: int,
            dfunc: Callable[..., Any],
            func: Callable[..., Coroutine[Any, Any, Sequence[Any]]],
            text: str,
            page: int = 0,
            **kwargs: Any
    ) -> AsyncDatabaseOffsetPagination:
        self.data[user_id] = AsyncDatabaseOffsetPagination(
            dfunc, func, text, page, **kwargs
        )

        return self.data[user_id]

    def get(self, user_id: int) -> Optional[AsyncDatabaseOffsetPagination]:
        return self.data.get(user_id)

    def clear(self, user_id: int) -> None:
        self.data.pop(user_id, None)
