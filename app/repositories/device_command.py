from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DeviceCommand
from app.repositories.base import BaseRepository


class DeviceCommandRepository(BaseRepository):
    model = DeviceCommand

    @classmethod
    async def get_pending(cls, db: AsyncSession):
        result = await db.execute(
            select(cls.model).
            where(cls.model.is_executed.is_(False)).
            order_by(cls.model.created_at.asc()).
            limit(50))
        return result.scalars().all()