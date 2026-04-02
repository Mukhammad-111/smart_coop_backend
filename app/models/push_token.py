import datetime
import enum

from sqlalchemy import (ForeignKey, Text, DateTime, func, Integer, Enum, Boolean,
                        UniqueConstraint, Index, text)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PushPlatform(enum.Enum):
    android = "android"
    ios = "ios"


class PushToken(Base):
    __tablename__ = "push_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE")
                                         , nullable=False)
    token: Mapped[str] = mapped_column(Text, nullable=False)
    platform: Mapped[PushPlatform] = mapped_column(
        Enum(PushPlatform, native_enum=False, length=10), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true", nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    __table_args__ = (
        UniqueConstraint("token", name="idx_push_tokens_token"),
        Index("idx_push_tokens_user_id", "user_id",
              postgresql_where=text("is_active = true")),
    )