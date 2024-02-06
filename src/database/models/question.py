from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger, ForeignKey, Enum
)

from src.database.models.base import Base
from src.database.models.base.mixins import ModelWithTimeMixin, ModelWithIDMixin
from src.utils.enums import Status

if TYPE_CHECKING:
    from src.database.models.user import User


class Question(ModelWithTimeMixin, ModelWithIDMixin, Base):
    user_message_id: Mapped[int] = mapped_column(BigInteger)
    admin_message_id: Mapped[int] = mapped_column(BigInteger)
    status: Mapped[Status] = mapped_column(
        Enum(Status)
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('user.id')
    )
    user: Mapped['User'] = relationship(
        'User',
        back_populates='questions'
    )
