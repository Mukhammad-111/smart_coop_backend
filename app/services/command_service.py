from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DeviceCommand, EventLog
from app.models.device_command import CommandType
from app.models.event_log import EventType, Severity
from app.models.system_mode import ChangeSource, SystemMode
from app.repositories.device_command import DeviceCommandRepository
from app.repositories.event_log import EventLogRepository
from app.repositories.feed_shedule import FeedScheduleRepository
from app.repositories.system_mode import SystemModeRepository
from app.schemas.command import (CommandStatusResponse, CommandAutoRequest, PendingCommandsResponse,
                                 CommandDoorRequest, \
    ActionItem, CommandDoorResponse)
from app.services.feed_schedule_service import get_feed_schedules
from app.services.mqtt_publisher import publish_command
from app.services.threshold_service import get_current_thresholds


async def command_pending_get_service(db: AsyncSession):
    commands = await DeviceCommandRepository.get_pending(db)

    thresholds = await get_current_thresholds(db)

    feed_schedule = await FeedScheduleRepository.get_active(db)

    return PendingCommandsResponse(
        commands=commands,
        thresholds=thresholds,
        feed_schedule=feed_schedule
    )


async def command_executed_service(command_id: int, db: AsyncSession):
    command = await DeviceCommandRepository.get_by_id(command_id, db)
    if command is None:
        raise HTTPException(status_code=404, detail="Command not found")

    command.is_executed = True
    command.executed_at = datetime.now(timezone.utc)
    await db.commit()
    return CommandStatusResponse(status="ok")


async def command_door_service(data: CommandDoorRequest, db: AsyncSession):
    if data.action == ActionItem.open:
        command_type = CommandType.door_open
        new_event_log = EventLog(event_type=EventType.door_open,
                                 severity=Severity.info,
                                 message="Door open")
    elif data.action == ActionItem.close:
        command_type = CommandType.door_close
        new_event_log = EventLog(event_type=EventType.door_close,
                                 severity=Severity.info,
                                 message="Door close")
    else:
        raise HTTPException(status_code=422, detail="Action must be open or close")

    new_command = DeviceCommand(command_type=command_type)

    created_command = await DeviceCommandRepository.create(new_command, db)
    await EventLogRepository.create(new_event_log, db)
    await db.commit()
    await db.refresh(created_command)

    await publish_command({
        "command_id": created_command.id,
        "command_type": command_type.value
    })

    return CommandDoorResponse(status="command_queued", command_id=created_command.id)


async def command_auto_service(data: CommandAutoRequest, db: AsyncSession):
    command = DeviceCommand(
        command_type=CommandType.set_auto,
        payload={"is_auto": data.is_auto}
    )
    await DeviceCommandRepository.create(command, db)

    last_mode = await SystemModeRepository.get_last(db)
    if last_mode is None:
        raise HTTPException(status_code=404, detail="Mode not found")

    new_mode = SystemMode(
        mode_name=last_mode.mode_name,
        is_auto=data.is_auto,
        changed_by=ChangeSource.user
    )
    await SystemModeRepository.create(new_mode, db)

    await db.commit()

    await publish_command({
        "command_type": "set_auto",
        "payload": {"is_auto": data.is_auto}
    })

    return CommandStatusResponse(status="command_queued")