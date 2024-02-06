import uuid

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class ModelWithUUIDMixin:
    """
    Base model class mixin that represents an ID field with a UUID type.

    Attributes:
        id (Mapped[uuid.UUID]): A mapped column representing the ID field with a UUID type.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        index=True,
    )
