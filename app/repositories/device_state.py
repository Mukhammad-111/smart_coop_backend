from sqlalchemy import select
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