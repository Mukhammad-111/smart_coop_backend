from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event_log import EventType
from app.repositories.event_log import EventLogRepository
from app.schemas.event_log import SeverityFilter, EventsResponse
from app.schemas.history import PeriodValue
from app.services.history import get_period_start


async def events_get_service(
        period: PeriodValue,
        severity: SeverityFilter,
        event_type: EventType,
        limit: int,
        offset: int,
        db: AsyncSession
):
    period_start = get_period_start(period)

    data = await EventLogRepository.get_filtered(
        period_start,
        severity,
        event_type,
        limit,
        offset,
        db
    )
    count = await EventLogRepository.get_count(period_start, severity, event_type, db)

    return EventsResponse(
        events=data,
        count=count
    )