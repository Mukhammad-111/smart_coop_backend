from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import List

from app.models.feed_schedule import FeedSchedule
from app.models.device_command import DeviceCommand, CommandType
from app.models.event_log import EventLog, EventType, Severity
from app.repositories.event_log import EventLogRepository
from app.schemas.feed_shedule import (
    FeedScheduleItem,
    FeedScheduleCreateRequest,
    FeedScheduleUpdateRequest,
    FeedTriggerRequest,
    FeedTriggerResponse
)
from app.repositories.feed_shedule import FeedScheduleRepository
from app.repositories.device_command import DeviceCommandRepository


async def get_feed_schedules(db: AsyncSession) -> List[FeedScheduleItem]:
    schedules = await FeedScheduleRepository.get_all(db)
    return schedules


async def create_feed_schedule(data: FeedScheduleCreateRequest, db: AsyncSession) -> FeedScheduleItem:
    if data.duration_seconds < 1 or data.duration_seconds > 60:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duration must be between 1 and 60 seconds"
        )

    schedule = FeedSchedule(
        feed_time=data.feed_time,
        duration_seconds=data.duration_seconds,
        is_active=data.is_active
    )
    created = await FeedScheduleRepository.create(schedule, db)
    await db.commit()
    await db.refresh(created)
    return created


async def update_feed_schedule(schedule_id: int, data: FeedScheduleUpdateRequest, db: AsyncSession) -> FeedScheduleItem:
    schedule = await FeedScheduleRepository.get_by_id(schedule_id, db)
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")

    if data.duration_seconds < 1 or data.duration_seconds > 60:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duration must be between 1 and 60 seconds"
        )

    updated = await FeedScheduleRepository.update(schedule, data, db)
    await db.commit()
    await db.refresh(updated)
    return updated


async def delete_feed_schedule(schedule_id: int, db: AsyncSession) -> None:
    schedule = await FeedScheduleRepository.get_by_id(schedule_id, db)
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")

    await FeedScheduleRepository.delete(schedule, db)
    await db.commit()


async def trigger_feed(data: FeedTriggerRequest, user_id: int, db: AsyncSession) -> FeedTriggerResponse:
    if data.duration_seconds < 1 or data.duration_seconds > 60:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duration must be between 1 and 60 seconds"
        )


    command = DeviceCommand(
        command_type=CommandType.feed_now,
        payload={"duration_seconds": data.duration_seconds}
    )
    created_command = await DeviceCommandRepository.create(command, db)
    await db.flush()


    event = EventLog(
        event_type=EventType.feed_triggered,
        severity=Severity.info,
        message=f"Feed triggered manually by user {user_id}",
        value=None
    )
    await EventLogRepository.create(event, db)

    await db.commit()

    return FeedTriggerResponse(
        status="command_queued",
        command_id=created_command.id
    )