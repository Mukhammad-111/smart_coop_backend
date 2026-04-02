import datetime
import enum

from sqlalchemy import BigInteger, DateTime, Enum, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class DoorStatus(enum.Enum):
    open = "open"
    closed = "closed"
    moving_open = "moving_open"
    moving_closed = "moving_closed"


class DeviceState(Base):
    __tablename__ = "device_states"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    heater: Mapped[bool] = mapped_column(Boolean, nullable=False)
    ventilation: Mapped[bool] = mapped_column(Boolean, nullable=False)
    lighting: Mapped[bool] = mapped_column(Boolean, nullable=False)
    door: Mapped[DoorStatus] = mapped_column(
        Enum(DoorStatus, native_enum=False, length=20),
        nullable=False, default=DoorStatus.closed, server_default="closed")
    feeder: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false")
    recorded_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now())