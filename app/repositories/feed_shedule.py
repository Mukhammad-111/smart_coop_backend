from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.models.feed_schedule import FeedSchedule


class FeedScheduleRepository(BaseRepository):
    model = FeedSchedule

    @classmethod
    async def get_active(cls, db: AsyncSession):
        result = await db.execute(select(cls.model).where(cls.model.is_active.is_(True)))
        return result.scalars().all()