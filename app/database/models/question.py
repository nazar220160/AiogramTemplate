from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import (
    Boolean,
    BigInteger,
)

from app.database.models.base import ModelWithID, Base


class Question(Base, ModelWithID):
    user_message_id: Mapped[int] = mapped_column(BigInteger)
    admin_message_id: Mapped[int] = mapped_column(BigInteger)
    answered: Mapped[bool] = mapped_column(Boolean, default=False)
