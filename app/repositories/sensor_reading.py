from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.models import SensorReading
from app.repositories.base import BaseRepository


class SensorRepository(BaseRepository):
    model = SensorReading

    @classmethod
    async def get_last_reading(cls, db: AsyncSession) -> SensorReading | None:
        result = await db.execute(
            select(cls.model).
            order_by(desc(cls.model.recorded_at))
            .limit(1))
        return result.scalar_one_or_none()

    @classmethod
    async def get_data_by_period(
            cls,
            period_start: datetime,
            limit: int,
            offset: int,
            db: AsyncSession):
        result = await db.execute(
            select(cls.model)
            .where(cls.model.recorded_at >= period_start)
            .order_by(cls.model.recorded_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    @classmethod
    async def get_count(cls, period_start: datetime,
                         db: AsyncSession):
        count_stmt = select(func.count()).where(
            cls.model.recorded_at >= period_start
        )

        return await db.scalar(count_stmt)

    @classmethod
    async def get_stats(cls, period_start: datetime, db: AsyncSession):
        stats_stmt = select(
            func.min(cls.model.temperature),
            func.max(cls.model.temperature),
            func.round(func.avg(cls.model.temperature), 1),

            func.min(cls.model.humidity),
            func.max(cls.model.humidity),
            func.round(func.avg(cls.model.humidity), 1),

            func.min(cls.model.light_level),
            func.max(cls.model.light_level),
            func.round(func.avg(cls.model.light_level), 1),
        ).where(cls.model.recorded_at >= period_start)

        result = await db.execute(stats_stmt)

        return result.one()