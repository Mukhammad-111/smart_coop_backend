import datetime
import enum
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, String, Enum, Numeric, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class EventSeverity(enum.Enum):
    info = "info"
    warning = "warning"
    critical = "critical"
    all = "all"


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[EventSeverity] = mapped_column(
        Enum(EventSeverity, native_enum=False, length=20),
        nullable=False, default=EventSeverity.all)
    message: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[Optional[Decimal]] = mapped_column(Numeric(6,2), nullable=True)
    occurred_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    __table_args__ = (
        Index("idx_events_occurred_at", occurred_at.desc()),
    )