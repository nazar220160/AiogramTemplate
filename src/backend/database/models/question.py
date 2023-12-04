from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger, ForeignKey, Enum
)

from src.backend.database.models.base import ModelWithID, ModelWithTime, Base
from src.backend.utils.enums import Status

if TYPE_CHECKING:
    from src.backend.database.models.user import User


class Question(Base, ModelWithID, ModelWithTime):
    user_message_id: Mapped[int] = mapped_column(BigInteger)
    admin_message_id: Mapped[int] = mapped_column(BigInteger)
    status: Mapped[Status] = mapped_column(
        Enum(Status)
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('user.user_id')
    )
    user: Mapped['User'] = relationship(
        'User',
        back_populates='questions'
    )
