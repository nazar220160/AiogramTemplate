import abc
from typing import Any, Protocol


class Handler(Protocol):
    """
    An abstract base class defining the protocol for handler classes.

    This class uses Python's typing.Protocol to define a contract that handler classes must follow.
    It specifies two abstract methods, '__call__' and 'handle', that need to be implemented by any
    concrete class adhering to this protocol. This ensures consistency and predictability in how
    handlers are used throughout the application.

    The Handler class is designed to be used in situations where handling various types of queries
    or requests in an asynchronous manner is required, such as in a command-query separation architecture.
    """

    @abc.abstractmethod
    async def __call__(self, query: Any) -> Any:
        """
        Abstract method to make the handler instance callable.

        This method should be implemented to allow instances of the implementing class to be called
        as a function, taking a query as an argument and returning a response.

        Args:
            query (Any): The query or request to be handled.

        Returns:
            Any: The result of handling the query.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def handle(self, query: Any) -> Any:
        """
        Abstract method defining the handling logic for a query or request.

        Implementing classes should provide the specific logic for handling the given query within
        this method. This is separate from the '__call__' method to provide clear semantics and the
        possibility of additional processing or routing logic in '__call__'.

        Args:
            query (Any): The query or request to be handled.

        Returns:
            Any: The result of handling the query.
        """
        raise NotImplementedError
