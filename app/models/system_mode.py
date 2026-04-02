import datetime
import enum

from sqlalchemy import String, Enum, DateTime, func, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class FSMMode(enum.Enum):
    day_moderate = "day_moderate"
    day_frost = "day_frost"
    night_cold = "night_cold"
    overheat = "overheat"
    manual = "manual"


class ChangeSource(enum.Enum):
    system = "system"
    user = "user"


class SystemMode(Base):
    __tablename__ = "system_modes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mode_name: Mapped[FSMMode] = mapped_column(
        Enum(FSMMode, native_enum=False, length=50), nullable=False)
    is_auto: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true")
    changed_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now())
    changed_by: Mapped[ChangeSource] = mapped_column(
        Enum(ChangeSource, native_enum=False, length=50),
        nullable=False, default=ChangeSource.system, server_default="system")