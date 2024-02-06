from typing import Optional

from sqlalchemy import JSON, BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base
from src.database.models.base.mixins import ModelWithTimeMixin


class BotChats(ModelWithTimeMixin, Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    title: Mapped[str] = mapped_column(String(255))

    permissions: Mapped[dict] = mapped_column(JSON)
    sub: Mapped[bool] = mapped_column(Boolean, default=False)
