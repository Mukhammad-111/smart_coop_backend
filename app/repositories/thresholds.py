from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Threshold
from app.repositories.base import BaseRepository


class ThresholdRepository(BaseRepository):
    model = Threshold

    @classmethod
    async def get_active(cls, db: AsyncSession):
        result = await db.execute(select(cls.model).where(cls.model.id == 1))
        return result.scalar_one_or_none()