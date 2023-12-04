from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import (
    String,
    BigInteger,
    Boolean
)

from src.database.models.base import Base


class ComSubChats(Base):
    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    turn: Mapped[Optional[bool]] = mapped_column(Boolean, default=True)
