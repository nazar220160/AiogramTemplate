from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class ModelWithIDMixin:
    """
    Base model class mixin that represents an ID field with an integer type.

    Attributes:
        id (Mapped[int]): A mapped column representing the ID field with an integer type.
    """

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
