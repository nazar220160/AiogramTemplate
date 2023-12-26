from typing import Optional, List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import (
    String,
    Boolean,
    BigInteger,
)

from src.database.models.base import ModelWithTime, Base

if TYPE_CHECKING:
    from src.database.models.question import Question


class User(Base, ModelWithTime):
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
    )
    first_name: Mapped[str] = mapped_column(String(64))
    username: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    language_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_premium: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    admin: Mapped[bool] = mapped_column(Boolean, default=False)

    questions: Mapped[List['Question']] = relationship(
        'Question',
        back_populates='user'
    )
