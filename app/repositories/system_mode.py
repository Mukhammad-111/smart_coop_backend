from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SystemMode
from app.repositories.base import BaseRepository


class SystemModeRepository(BaseRepository):
    model = SystemMode

    @classmethod
    async def get_last(cls, db: AsyncSession):
        result = await db.execute(
            select(cls.model).
            order_by(cls.model.changed_at.desc()).
            limit(1)
        )

        return result.scalars().first()