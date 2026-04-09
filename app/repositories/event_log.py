from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import EventLog
from app.repositories.base import BaseRepository
from datetime import datetime

from app.schemas.event_log import SeverityFilter


class EventLogRepository(BaseRepository):
    model = EventLog

    @classmethod
    async def get_filtered(
            cls,
            period_start: datetime,
            severity,
            event_type,
            limit: int,
            offset: int,
            db: AsyncSession
    ):
        stmt = select(cls.model)

        stmt = stmt.where(cls.model.occurred_at >= period_start)

        if severity != SeverityFilter.all:
            stmt = stmt.where(cls.model.severity == severity.value)

        if event_type:
            stmt = stmt.where(cls.model.event_type == event_type)

        stmt = stmt.order_by(cls.model.occurred_at.desc()).limit(limit).offset(offset)

        result = await db.execute(stmt)

        return result.scalars().all()

    @classmethod
    async def get_count(
            cls,
            period_start: datetime,
            severity,
            event_type,
            db: AsyncSession
    ):
        stmt = select(func.count()).where(
            cls.model.occurred_at >= period_start
        )
        if severity != SeverityFilter.all:
            stmt = stmt.where(cls.model.severity == severity.value)

        if event_type:
            stmt = stmt.where(cls.model.event_type == event_type)

        return await db.scalar(stmt)