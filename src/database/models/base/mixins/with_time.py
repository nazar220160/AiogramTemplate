from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class ModelWithTimeMixin:
    """
    Base model class mixin that includes timestamp fields for creation, update, and deletion times.

    Attributes:
        created_at (Mapped[datetime]): A mapped column representing the creation timestamp.
        updated_at (Mapped[datetime]): A mapped column representing the last update timestamp.
        deleted_at (Mapped[datetime]): A mapped column representing the timestamp of deletion (nullable).
    """

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        onupdate=func.now(),
        server_default=func.now(),
    )
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
