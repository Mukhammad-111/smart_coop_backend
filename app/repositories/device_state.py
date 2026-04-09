from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DeviceState
from app.repositories.base import BaseRepository


class DeviceStateRepository(BaseRepository):
    model = DeviceState

    @classmethod
    async def get_first(cls, db: AsyncSession):
        return await db.scalar(select(cls.model).limit(1))


    @classmethod
    async def get_last(cls, db: AsyncSession):
        result = await db.execute(
            select(cls.model).
            order_by(cls.model.recorded_at.desc()).
            limit(1))

        return result.scalars().first()

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
    async def get_count(
            cls,
            period_start: datetime,
            db: AsyncSession
    ):
        stmt = select(func.count()).where(
            cls.model.recorded_at >= period_start
        )
        return await db.scalar(stmt)