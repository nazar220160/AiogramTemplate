from typing import Any, Dict

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models providing common functionality such as automatic table name generation,
    a human-readable representation, and a method to convert the object to a dictionary.

    Attributes:
        __abstract__ (bool): Indicates that this class is abstract and should not be used for database table mapping.
    """

    __abstract__: bool = True

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        """
        Generate the default table name for the SQLAlchemy model based on the class name.

        Returns:
            str: The table name generated from the class name in lowercase.
        """
        return cls.__name__.lower()

    def __repr__(self) -> str:
        """
        Return a human-readable representation of the object.

        Returns:
            str: A string representation of the object containing its class name and non-private attributes.
        """
        params = ", ".join(
            f"{attr}={value!r}"
            for attr, value in self.__dict__.items()
            if not attr.startswith("_")
        )
        return f"{type(self).__name__}({params})"

    def as_dict(self) -> Dict[str, Any]:
        """
        Convert the object to a dictionary containing non-private attributes and their values.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            attr: value
            for attr, value in self.__dict__.items()
            if not attr.startswith("_")
        }
