from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

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