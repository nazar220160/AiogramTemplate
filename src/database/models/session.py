from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base
from src.database.models.base.mixins import ModelWithIDMixin, ModelWithTimeMixin

if TYPE_CHECKING:
    from src.database.models.dialog import Dialog
    from src.database.models.user import User


class Session(ModelWithTimeMixin, ModelWithIDMixin, Base):
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("user.id"))
    phone_number: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    session: Mapped[str] = mapped_column(String(362), unique=True)
    proxy: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=None)
    test_net: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship("User", back_populates="sessions")
    dialogs: Mapped[List["Dialog"]] = relationship("Dialog", back_populates="session")
