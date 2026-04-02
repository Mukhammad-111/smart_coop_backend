import datetime
import enum
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, Enum, Text, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class EventType(enum.Enum):
    alarm_temp_high = "alarm_temp_high"
    alarm_temp_low = "alarm_temp_low"
    alarm_humidity = "alarm_humidity"
    mode_change = "mode_change"
    door_open = "door_open"
    door_close = "door_close"
    feed_triggered = "feed_triggered"
    device_online = "device_online"
    device_offline = "device_offline"
    sensor_error = "sensor_error"
    camera_offline = "camera_offline"


class Severity(enum.Enum):
    info = "info"
    warning = "warning"
    critical = "critical"


class EventLog(Base):
    __tablename__ = "event_log"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    event_type: Mapped[EventType] = mapped_column(
        Enum(EventType, native_enum=False, length=50), nullable=False)
    severity: Mapped[Severity] = mapped_column(
        Enum(Severity, native_enum=False, length=20),
        nullable=False, default=Severity.info, server_default="info")
    message: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 2), nullable=True)
    occurred_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )