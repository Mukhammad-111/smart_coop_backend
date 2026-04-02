import datetime
from decimal import Decimal
from sqlalchemy import DateTime, func, BigInteger, Numeric, Integer, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.database.base import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True,
        comment="Уникальный идентификатор записи. BIGSERIAL — для больших объёмов")
    temperature: Mapped[Optional[Decimal]] = mapped_column(Numeric(5,2),
        nullable=True,
        comment="Температура воздуха в °C. Диапазон: -40.00 … +85.00. NULL если датчик DHT22 вернул ошибку.")
    humidity: Mapped[Optional[Decimal]] = mapped_column(Numeric(5,2),
        nullable=True,
        comment="Относительная влажность в %. Диапазон: 0.00 … 100.00. NULL если датчик DHT22 вернул ошибку.")
    light_level: Mapped[ Optional[int]] = mapped_column(Integer,
        nullable=True,
        comment="Освещённость в люксах. Диапазон: 0 … 65535. NULL если датчик BH1750 вернул ошибку.")
    recorded_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Метка времени записи в UTC. DEFAULT NOW() — проставляется сервером при получении данных."
    )
    __table_args__ = (
        Index("idx_sensor_readings_recorded_at", recorded_at.desc()),
        CheckConstraint("temperature >= -40 AND temperature <= 85", name="check_temp_range"),
        CheckConstraint("humidity >= 0 AND humidity <= 100", name="check_humidity_range"),
    )