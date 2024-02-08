from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON, BigInteger, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base
from src.database.models.base.mixins import ModelWithIDMixin, ModelWithTimeMixin

if TYPE_CHECKING:
    from src.database.models.session import Session


class Dialog(ModelWithTimeMixin, ModelWithIDMixin, Base):
    user_id: Mapped[int] = mapped_column(BigInteger)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("session.id"))
    chat_id: Mapped[int] = mapped_column(BigInteger)
    chat_username: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    chat_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    chat_type: Mapped[str] = mapped_column(Text)
    admin_rights: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    members_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    session: Mapped["Session"] = relationship("Session", back_populates="dialogs")
