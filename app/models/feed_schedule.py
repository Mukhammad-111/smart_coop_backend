import datetime

from sqlalchemy import Integer, Time, Boolean, DateTime, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class FeedSchedule(Base):
    __tablename__ = "feed_schedule"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    feed_time: Mapped[datetime.time] = mapped_column(
        Time(timezone=False), nullable=False,
        comment="Время кормления в формате HH:MM:SS (UTC). ESP32 сравнивает с текущим временем NTP.")
    duration_seconds: Mapped[int] = mapped_column(
        Integer, nullable=False, default=5, server_default="5")
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true")
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    __table_args__ = (
        CheckConstraint("duration_seconds BETWEEN 1 AND 60", name="check_duration_range")
    )