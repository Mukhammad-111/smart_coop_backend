import datetime
from decimal import Decimal
from sqlalchemy import Integer, DateTime, func, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Threshold(Base):
    __tablename__ = "thresholds"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=False, default=1, server_default="1")
    t_comfort_min: Mapped[Decimal] = mapped_column(Numeric(5, 2),
        default=Decimal("18.0"), server_default="18.0", comment="Нижняя граница комфортной температуры.")
    t_comfort_max: Mapped[Decimal] = mapped_column(Numeric(5, 2),
        default=Decimal("24.0"), server_default="24.0", comment="Верхняя граница комфортной температуры.")
    t_low_on: Mapped[Decimal] = mapped_column(Numeric(5, 2),
        default=Decimal("10.0"), server_default="10.0", comment="Порог входа в дневной морозный режим.")
    t_low_off: Mapped[Decimal] = mapped_column(Numeric(5, 2),
        default=Decimal("12.0"), server_default="12.0", comment="Порог выхода из морозного режима (гистерезис).")
    t_high_on: Mapped[Decimal] = mapped_column(Numeric(5, 2),
        default=Decimal("30.0"), server_default="30.0", comment="Порог входа в режим перегрева.")
    t_high_off: Mapped[Decimal] = mapped_column(Numeric(5, 2),
        default=Decimal("28.0"), server_default="28.0", comment="Порог выхода из режима перегрева (гистерезис).")
    t_critical_low: Mapped[Decimal] = mapped_column(
        Numeric(5,2), default=Decimal("3.0"), server_default="3.0",
        comment="Критически низкая температура. Аварийный обогрев принудительно включается даже в ручном режиме.")
    t_critical_high: Mapped[Decimal] = mapped_column(
        Numeric(5,2), default=Decimal("35.0"), server_default="35.0",
        comment="Критически высокая температура. Аварийное охлаждение принудительно включается даже в ручном режиме.")
    h_normal_max: Mapped[Decimal] = mapped_column(Numeric(5,2),
        default=Decimal("70.0"), server_default="70.0", comment="Порог включения вентиляции по влажности.")
    h_normal_min: Mapped[Decimal] = mapped_column(Numeric(5,2),
        default=Decimal("60.0"), server_default="60.0", comment="Порог выключения вентиляции по влажности (гистерезис).")
    h_critical: Mapped[Decimal] = mapped_column(Numeric(5,2),
        default=Decimal("85.0"), server_default="85.0",
        comment="Критическая влажность — аварийная принудительная вентиляция, push-уведомление severity=critical.")
    lux_day_on: Mapped[int] = mapped_column(Integer,
        default=200, server_default="200", comment="Порог определения дневного времени суток.")
    lux_day_off: Mapped[int] = mapped_column(Integer,
        default=150, server_default="150", comment="Порог определения ночного времени (гистерезис).")
    lux_light_on: Mapped[int] = mapped_column(Integer,
        default=300, server_default="300", comment="Порог включения искусственного освещения.")
    lux_light_off: Mapped[int] = mapped_column(Integer,
        default=350, server_default="350", comment="Порог выключения освещения (гистерезис).")
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    __table_args__ = (
        # 1. Запрещаем создавать более одной записи (только id=1)
        CheckConstraint('id = 1', name='check_only_one_row'),
        # 2. Проверяем логику гистерезиса (по желанию, но полезно)
        CheckConstraint('t_low_off > t_low_on', name='check_t_low_hysteresis'),
        CheckConstraint('t_high_on > t_high_off', name='check_t_high_hysteresis'),
        CheckConstraint('lux_day_on > lux_day_off', name='check_lux_day_hysteresis'),
    )