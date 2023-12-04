from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger, ForeignKey, Enum
)

from src.database.models.base import ModelWithID, ModelWithTime, Base
from src.utils.enums import Status

if TYPE_CHECKING:
    from src.database.models.user import User


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
