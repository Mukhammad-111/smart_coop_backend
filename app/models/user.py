import datetime

from sqlalchemy import String, DateTime, func, Integer, Boolean, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true", nullable=False)
    notif_alarm_temp_high: Mapped[bool] = mapped_column(Boolean,
        default=True, server_default="true", nullable=False,
        comment="Получать push при высокой/критической температуре")
    notif_alarm_temp_low: Mapped[bool] = mapped_column(Boolean,
        default=True, server_default="true", nullable=False,
        comment="Получать push при низкой/критической температуре")
    notif_alarm_humidity: Mapped[bool] = mapped_column(Boolean,
        default=True, server_default="true", nullable=False,
        comment="Получать push при высокой/критической влажности")
    notif_door_state: Mapped[bool] = mapped_column(Boolean,
        default=True, server_default="true", nullable=False,
        comment="Получать push при изменении состояния двери")
    notif_device_offline: Mapped[bool] = mapped_column(Boolean,
        default=True, server_default="true", nullable=False,
        comment="Получать push когда ESP32 перестаёт")
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    __table_args__ = (
        CheckConstraint("char_length(first_name) >= 2", name="check_first_name_len"),
        CheckConstraint("char_length(last_name) >= 2", name="check_last_name_len"),
    )