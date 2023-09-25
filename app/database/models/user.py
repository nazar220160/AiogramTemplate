from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import (
    String,
    Boolean,
    BigInteger,
)

from app.database.models.base import ModelWithTime, Base


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
    admin: Mapped[bool] = mapped_column(Boolean, default=False)
